import aiohttp
import socket
import ipaddress
import urllib.parse
from dataclasses import dataclass
from typing import Optional
import asyncio

@dataclass
class FetchResult:
    status: str # SUCCESS, FAILED, TIMEOUT, UNAVAILABLE
    content: Optional[str] = None
    error_message: Optional[str] = None
    final_url: Optional[str] = None

class SafeResolver(aiohttp.resolver.ThreadedResolver):
    async def resolve(self, host, port=0, family=socket.AF_INET):
        # Delegate to aiohttp's built-in threaded resolver
        hosts = await super().resolve(host, port, family)
        
        safe_hosts = []
        for h in hosts:
            if SafeFetcher.is_ip_safe(h['host']):
                safe_hosts.append(h)
                
        if not safe_hosts:
            raise ValueError(f"SSRF protection blocked the request: Unsafe IP resolved for {host}")
            
        return safe_hosts

class SafeFetcher:
    MAX_REDIRECTS = 3
    MAX_SIZE_BYTES = 5 * 1024 * 1024 # 5 MB
    TIMEOUT = 10.0
    
    @staticmethod
    def is_ip_safe(ip_str: str) -> bool:
        try:
            ip = ipaddress.ip_address(ip_str)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved or ip.is_unspecified:
                return False
            # Check specifically for cloud metadata IP
            if ip_str == "169.254.169.254":
                return False
            # IPv6 mapped metadata IP handling
            if hasattr(ip, "ipv4_mapped") and ip.ipv4_mapped:
                return SafeFetcher.is_ip_safe(str(ip.ipv4_mapped))
            return True
        except ValueError:
            return False

    @classmethod
    async def fetch(cls, url: str) -> FetchResult:
        if not url.startswith("https://"):
            return FetchResult(status="FAILED", error_message="URL must use HTTPS")
            
        current_url = url
        redirects_followed = 0
        
        # We use a custom resolver to eliminate the TOCTOU DNS rebinding vulnerability.
        # This ensures the underlying TCP socket connects EXACTLY to the IP we validated.
        resolver = SafeResolver()
        connector = aiohttp.TCPConnector(resolver=resolver)
        timeout = aiohttp.ClientTimeout(total=cls.TIMEOUT)
        
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                while redirects_followed <= cls.MAX_REDIRECTS:
                    try:
                        async with session.get(current_url, allow_redirects=False) as response:
                            if response.status in (301, 302, 303, 307, 308):
                                redirects_followed += 1
                                next_url = response.headers.get("Location")
                                if not next_url:
                                    return FetchResult(status="FAILED", error_message="Redirect missing Location header")
                                current_url = urllib.parse.urljoin(current_url, next_url)
                                if not current_url.startswith("https://"):
                                    return FetchResult(status="FAILED", error_message="Redirected to non-HTTPS URL")
                                continue
                                
                            response.raise_for_status()
                            
                            content_bytes = bytearray()
                            async for chunk in response.content.iter_chunked(8192):
                                content_bytes.extend(chunk)
                                if len(content_bytes) > cls.MAX_SIZE_BYTES:
                                    return FetchResult(status="FAILED", error_message="Response exceeded maximum allowed size")
                                    
                            content_str = content_bytes.decode("utf-8", errors="replace")
                            return FetchResult(
                                status="SUCCESS", 
                                content=content_str,
                                final_url=current_url
                            )
                            
                    except aiohttp.ClientResponseError as e:
                        return FetchResult(status="UNAVAILABLE", error_message=f"HTTP Error: {e.status}")
        except asyncio.TimeoutError:
            return FetchResult(status="TIMEOUT", error_message="Connection timed out")
        except Exception as e:
            if "SSRF protection" in str(e):
                return FetchResult(status="FAILED", error_message=str(e))
            return FetchResult(status="FAILED", error_message=f"Fetch failed: {str(e)}")
            
        return FetchResult(status="FAILED", error_message="Too many redirects")
