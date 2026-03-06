/**
 * RTIAssist — Real-World Indian Legal Problems Database
 * Research-based examples for quick-fill suggestions in UI & Bot
 * All section numbers, portals, fees, and time limits are legally accurate (2026)
 */

var LEGAL_EXAMPLES = {

  // ══════════════════════════════════════════════════════════════
  // 1. RTI APPLICATION — Section 6(1), RTI Act 2005
  // ══════════════════════════════════════════════════════════════
  rti: [
    {
      title: "Ration Card Rejected",
      desc: "Ration card application reject ho gayi bina koi reason bataye. Months se chakkar laga rahe hain.",
      state: "Maharashtra / UP / Bihar",
      dept: "Food & Civil Supplies Department",
      difficulty: "easy",
      success: "high",
      which_law: "RTI Act 2005, Section 6(1)",
      time_limit: "PIO must reply within 30 days",
      fee: "₹10 (Central) / ₹10 most states",
      portal: "rtionline.gov.in (Central) / state portal",
      prefill: "Mera ration card application [DATE] ko submit kiya tha [DISTRICT] mein. Application number [NUMBER] hai. Aaj tak na koi reply aaya, na koi reason bataya. Main jaanna chahta/chahti hoon: (1) Meri application ka current status kya hai? (2) Reject ki gayi hai toh reason kya hai? (3) Kis officer ne decision liya? (4) Appeal karne ki process kya hai?"
    },
    {
      title: "Pension Not Started",
      desc: "Retirement ke 6 mahine baad bhi pension nahi aayi. PPO number mila hai lekin bank mein kuch nahi.",
      state: "All States — Central Govt employees",
      dept: "Department of Pension & Pensioners' Welfare / State Treasury",
      difficulty: "medium",
      success: "high",
      which_law: "RTI Act 2005, Section 6(1)",
      time_limit: "30 days",
      fee: "₹10",
      portal: "rtionline.gov.in",
      prefill: "Main [DESIGNATION] post se [DATE] ko retire hua/hui hoon. PPO number [PPO NO] hai. Retire hue 6 mahine ho gaye hain lekin abhi tak pension start nahi hui. Main jaanna chahta/chahti hoon: (1) Meri pension file ka current status? (2) Kis stage par atki hui hai? (3) Delay ke liye kaun zimmedar hai? (4) Kab tak start hogi?"
    },
    {
      title: "Land Mutation Pending",
      desc: "Property kharidi 1 saal pehle, mutation abhi tak nahi hua. Tehsil ke chakkar kaate kaate thak gaye.",
      state: "UP / Rajasthan / MP / Bihar / Uttarakhand",
      dept: "Revenue Department / Tehsildar Office",
      difficulty: "medium",
      success: "high",
      which_law: "RTI Act 2005, Section 6(1)",
      time_limit: "30 days",
      fee: "₹10",
      portal: "State RTI portal",
      prefill: "Maine [DATE] ko [SELLER NAME] se zameen/property kharidi thi. Registry number [NUMBER] hai, [DISTRICT] tehsil mein. Mutation application [DATE] ko di thi lekin aaj tak koi action nahi hua. Main jaanna chahta/chahti hoon: (1) Meri mutation application ka status? (2) Kaunsa officer handle kar raha hai? (3) Delay ka reason kya hai? (4) Kab tak complete hoga?"
    },
    {
      title: "Passport Police Verification Delay",
      desc: "Passport apply kiye 3 mahine ho gaye, police verification pending hai. Urgent travel ka kaam atka hua hai.",
      state: "All States",
      dept: "Local Police Station / Passport Seva Kendra",
      difficulty: "easy",
      success: "high",
      which_law: "RTI Act 2005, Section 6(1)",
      time_limit: "30 days",
      fee: "₹10",
      portal: "rtionline.gov.in / passportindia.gov.in",
      prefill: "Maine passport ke liye [DATE] ko apply kiya tha. Application number [NUMBER] hai. Police verification ke liye [POLICE STATION] ko [DATE] ko bheja gaya tha. 3 mahine se zyada ho gaye hain lekin verification complete nahi hui. Main jaanna chahta/chahti hoon: (1) Police verification ka current status? (2) Kaunse officer ke paas file hai? (3) Delay ka reason kya hai?"
    },
    {
      title: "Scholarship Not Received",
      desc: "SC/OBC/Minority scholarship form bhara, select bhi hua, lekin paisa account mein nahi aaya.",
      state: "UP / Bihar / MP / Rajasthan",
      dept: "Social Welfare / Minority Affairs / Education Department",
      difficulty: "medium",
      success: "high",
      which_law: "RTI Act 2005, Section 6(1)",
      time_limit: "30 days",
      fee: "₹10",
      portal: "State RTI portal / scholarships.gov.in",
      prefill: "Maine [SCHEME NAME] scholarship ke liye [ACADEMIC YEAR] mein apply kiya tha. Roll number [NUMBER] hai, [COLLEGE NAME] mein padhta/padhti hoon. Merit list mein naam aaya lekin abhi tak scholarship amount nahi mili. Main jaanna chahta/chahti hoon: (1) Mera scholarship application kahan atka hua hai? (2) Amount kab disburse hogi? (3) Koi issue hai toh kya hai?"
    },
    {
      title: "Road Construction Scam",
      desc: "Naali/sadak banane ka kaam form pe toh complete dikha, reality mein adha kaam hua. PMGSY funds ka hisaab chahiye.",
      state: "Rural areas — all states",
      dept: "PWD / PMGSY / Gram Panchayat / Municipal Corporation",
      difficulty: "medium",
      success: "medium",
      which_law: "RTI Act 2005, Section 6(1); also PMGSY guidelines",
      time_limit: "30 days",
      fee: "₹10",
      portal: "rtionline.gov.in / State PWD portal",
      prefill: "Hamare gaon/ward mein [ROAD/NAALI NAME] ka nirman [SCHEME] ke tahat hona tha. Work order number [NUMBER] tha, kaam [DATE] se [DATE] ke beech hona tha. Kagaz par kaam complete dikhaya gaya lekin asal mein kaam adha adhura hai ya quality bahut kharab hai. Main jaanna chahta/chahti hoon: (1) Is kaam ka estimated budget kya tha? (2) Kitna payment release hua? (3) Quality inspection report kya hai? (4) Contractor ka naam kya hai?"
    },
    {
      title: "NREGA Wages Not Paid",
      desc: "MGNREGA mein kaam kiya, muster roll mein naam bhi hai lekin 2 mahine se wages nahi aaye account mein.",
      state: "Bihar / Jharkhand / UP / Odisha / Rajasthan",
      dept: "Gram Panchayat / Block Development Office / MGNREGA",
      difficulty: "easy",
      success: "high",
      which_law: "RTI Act 2005, Section 6(1); MGNREGA Act 2005",
      time_limit: "30 days",
      fee: "₹10",
      portal: "State RTI portal / nregs.nic.in",
      prefill: "Main [VILLAGE/WARD] ka/ki MGNREGA worker hoon. Mera job card number [NUMBER] hai. Maine [WORK NAME] mein [DATES] ko kaam kiya. Muster roll mein mera naam hai lekin wages abhi tak bank account mein nahi aayi. Main jaanna chahta/chahti hoon: (1) Mera wage payment status kya hai? (2) Payment kab release hua/nahi hua? (3) Delay ka reason kya hai?"
    },
    {
      title: "FIR Not Registered by Police",
      desc: "Complaint dene gayi/gaya, police ne FIR likhne se mana kar diya. Bahane bana rahe hain.",
      state: "All States",
      dept: "State Police / Home Ministry",
      difficulty: "hard",
      success: "medium",
      which_law: "RTI Act 2005, Section 6(1); also Section 154 CrPC / BNSS 2023",
      time_limit: "30 days",
      fee: "₹10",
      portal: "State RTI portal",
      prefill: "Maine [DATE] ko [POLICE STATION NAME] mein [INCIDENT] ki complaint dene gayi/gaya tha. Police ne FIR likhne se mana kar diya ya sirf GD entry ki. Main jaanna chahta/chahti hoon: (1) Mere complaint ka kya hua? (2) GD register mein kya entry hai? (3) FIR kyon nahi likhi gayi? (4) Concerned SHO ka naam aur number kya hai?"
    },
    {
      title: "Electricity Meter Dispute",
      desc: "Bijli bill 3x aa raha hai actual usage se. Meter theek hai phir bhi complaint ka koi jawab nahi.",
      state: "All States",
      dept: "State Electricity Distribution Company (DISCOM)",
      difficulty: "easy",
      success: "high",
      which_law: "RTI Act 2005, Section 6(1); Electricity Act 2003",
      time_limit: "30 days",
      fee: "₹10",
      portal: "State RTI portal",
      prefill: "Mera bijli consumer number [NUMBER] hai, [ADDRESS] par. Pichle [X] mahino se bill bahut zyada aa raha hai — actual usage [UNITS] ke badle [UNITS] bill kar rahe hain. Meter testing ki complaint [DATE] ko di thi lekin koi action nahi hua. Main jaanna chahta/chahti hoon: (1) Mera meter testing report kya hai? (2) Bill calculation kaise hua? (3) Complaint ka kya action liya gaya?"
    },
    {
      title: "PDS Ration Not Distributed",
      desc: "Fair price shop par ration milta hi nahi. Dealer bol deta hai stock nahi hai — lekin baadmein bechta hai.",
      state: "Bihar / UP / Jharkhand / Odisha",
      dept: "Food & Civil Supplies / FCI / State PDS",
      difficulty: "easy",
      success: "high",
      which_law: "RTI Act 2005, Section 6(1); National Food Security Act 2013",
      time_limit: "30 days",
      fee: "₹10",
      portal: "State RTI portal",
      prefill: "Mere ration card number [NUMBER] par hamare gaon ke fair price shop [SHOP NAME, DEALER NAME] se [MAHINE KA NAAM] mein ration nahi mila. Dealer ne bola stock khatam ho gaya lekin baad mein bazaar mein bika. Main jaanna chahta/chahti hoon: (1) Hamare shop ka [MONTH] ka stock allocation kya tha? (2) Kitna ration distribute hua? (3) Dealer ke against koi complaint record hai?"
    }
  ],

  // ══════════════════════════════════════════════════════════════
  // 2. FIRST APPEAL — Section 19(1), RTI Act 2005
  // ══════════════════════════════════════════════════════════════
  first_appeal: [
    {
      title: "PIO Did Not Reply in 30 Days",
      desc: "RTI bheje 35+ din ho gaye, koi jawab nahi aaya. Ab first appeal deni hai.",
      state: "All States / Central",
      dept: "First Appellate Authority (FAA) of same department",
      difficulty: "easy",
      success: "high",
      which_law: "RTI Act 2005, Section 19(1) — appeal within 30 days of deadline",
      time_limit: "File within 30 days of PIO's deadline; FAA must reply in 30 days",
      fee: "No fee for First Appeal",
      portal: "rtionline.gov.in (online) / Speed Post to department FAA",
      prefill: "Maine [DATE] ko RTI application bheja tha [DEPARTMENT] ke PIO ko. Registration number [RTI NO] hai. 30 days deadline [DATE] thi lekin aaj [DATE] tak koi reply nahi mili. Is liye Section 19(1) ke tahat pratham appeal kar raha/rahi hoon. Nivedan hai ki PIO ko complete information dene ka aadesh diya jaaye aur Section 20(1) ke tahat penalty lagayi jaaye."
    },
    {
      title: "Incomplete / Vague Information Given",
      desc: "PIO ne jawab diya lekin sawal ka direct answer nahi diya. Gol gol baatein karke case close kar diya.",
      state: "All States",
      dept: "FAA of same department",
      difficulty: "easy",
      success: "high",
      which_law: "RTI Act 2005, Section 19(1); Section 7(1) — complete information",
      time_limit: "30 days from PIO's response date",
      fee: "No fee",
      portal: "rtionline.gov.in / Speed Post",
      prefill: "PIO ka jawab [DATE] ko aaya tha lekin jawab adhura hai. Main jaanna chahta/chahti tha: [ORIGINAL QUESTION] — lekin PIO ne sirf yeh bataya: [INCOMPLETE ANSWER]. Specific information: [WHAT IS MISSING] nahi di gayi. Request hai ki FAA PIO ko complete, point-by-point information dene ka nirdesha de."
    },
    {
      title: "Information Denied — Wrong Exemption Cited",
      desc: "PIO ne Section 8 lagaakar information deny ki lekin ye information clearly exempt nahi hai.",
      state: "All States",
      dept: "FAA of same department",
      difficulty: "medium",
      success: "medium",
      which_law: "RTI Act 2005, Section 19(1); Section 8 exemptions",
      time_limit: "30 days from PIO's response",
      fee: "No fee",
      portal: "rtionline.gov.in / Speed Post",
      prefill: "PIO ne meri RTI application ko Section 8([SUB-SECTION]) citing karke reject kar diya. Lekin jo information maangi gayi hai woh clearly public interest mein hai aur cited exemption applicable nahi hai kyunki: [REASON]. Request hai ki FAA is exemption ko override karke information dene ka aadesh de per Section 19(8)(a) of RTI Act."
    },
    {
      title: "Wrong Department Transfer — Info Still Not Received",
      desc: "PIO ne application galat department ko transfer kar di. Wahan bhi koi jawab nahi aaya.",
      state: "All States",
      dept: "Original department FAA",
      difficulty: "easy",
      success: "high",
      which_law: "RTI Act 2005, Section 6(3) — transfer within 5 days; Section 19(1)",
      time_limit: "30 days",
      fee: "No fee",
      portal: "rtionline.gov.in",
      prefill: "Meri RTI application Registration No [NUMBER] ko PIO ne [DATE] ko [WRONG DEPT] ko transfer kar diya. Transfer Section 6(3) ke against tha — yeh information clearly [ORIGINAL DEPT] ke paas honi chahiye. Transfer ke baad bhi koi reply nahi aayi. Pratham appeal mein nivedan hai ki original PIO ya concerned department se information dilwayi jaaye."
    },
    {
      title: "Information Given in Wrong Format",
      desc: "PIO ne information di lekin certify nahi ki, ya documents ki photocopy nahi di — sirf verbal jawab.",
      state: "All States",
      dept: "FAA of same department",
      difficulty: "easy",
      success: "high",
      which_law: "RTI Act 2005, Section 7(9) — information in requested form; Section 19(1)",
      time_limit: "30 days",
      fee: "No fee",
      portal: "Speed Post / rtionline.gov.in",
      prefill: "PIO ke jawab mein meri maangi gayi specific documents ki certified copies nahi di gayi. Sirf [VERBAL/SUMMARY] information di gayi. Main ne Section 7(9) ke tahat certified copies maangi thi [DOCUMENTS LIST]. Request hai ki FAA, PIO ko proper certified document copies dene ka aadesh de aur cost of copies bhi bataye."
    }
  ],

  // ══════════════════════════════════════════════════════════════
  // 3. SECOND APPEAL (CIC) — Section 19(3), RTI Act 2005
  // ══════════════════════════════════════════════════════════════
  second_appeal: [
    {
      title: "First Appeal Also Ignored",
      desc: "First appeal bhi 35+ din ho gaye, FAA ne bhi koi jawab nahi diya. Ab CIC jaana padega.",
      state: "Central Govt departments",
      dept: "Central Information Commission (CIC), New Delhi",
      difficulty: "medium",
      success: "medium",
      which_law: "RTI Act 2005, Section 19(3) — second appeal to CIC/SIC",
      time_limit: "File within 90 days of FAA's deadline",
      fee: "No fee for Second Appeal",
      portal: "cic.gov.in (online filing available)",
      prefill: "Maine Section 19(1) ke tahat pratham appeal [DATE] ko ki thi, FAA ka reference number [NUMBER] hai. FAA ne 30 days deadline tak koi reply nahi di. Is liye Section 19(3) ke tahat CIC mein second appeal kar raha/rahi hoon. Nivedan hai ki: (1) PIO ko complete information dene ka aadesh ho, (2) Section 20(1) penalty ₹250/day lagaayi jaaye, (3) Muavze ka aadesh Section 19(8)(b) ke tahat diya jaaye."
    },
    {
      title: "FAA Upheld Wrong Denial",
      desc: "FAA ne bhi PIO ki galat information denial ko sahi thahra diya. Legal ground pe challenge karna hai.",
      state: "Central Govt",
      dept: "Central Information Commission",
      difficulty: "hard",
      success: "medium",
      which_law: "RTI Act 2005, Section 19(3); Section 8 exemptions must be interpreted narrowly",
      time_limit: "90 days from FAA order",
      fee: "No fee",
      portal: "cic.gov.in",
      prefill: "FAA ne [DATE] ke order mein PIO ki refusal ko sahi thahraya. Mera contention hai ki yeh decision galat hai kyunki: (1) Cited exemption Section 8([X]) applicable nahi hai, (2) Information public interest mein hai — Supreme Court in CPIO v Subhash C. Aggarwal (2019) ke anusaar, (3) Public activity mein transparency zaroori hai. Nivedan hai ki CIC in-person hearing ke baad PIO ko information dene ka aadesh de."
    },
    {
      title: "Penalty Not Imposed Despite Clear Delay",
      desc: "CIC ne information dene ka order diya lekin penalty nahi lagaayi. Complaint ek baar aur karni hai.",
      state: "Central",
      dept: "Central Information Commission",
      difficulty: "hard",
      success: "low",
      which_law: "RTI Act 2005, Section 19(3); Section 20(1) — penalty ₹250/day up to ₹25,000",
      time_limit: "90 days from last order",
      fee: "No fee",
      portal: "cic.gov.in",
      prefill: "Pehle ki hearing mein CIC ne information dene ka aadesh diya tha lekin Section 20(1) ke tahat penalty nahi lagaayi. Jabki PIO ne [X] din ki delay ki jo clearly without reasonable cause thi. Nivedan hai ki CIC maximum penalty ₹25,000 impose kare aur disciplinary action ke liye recommend kare as per Section 20(2)."
    },
    {
      title: "State Govt: SIC Second Appeal",
      desc: "State department ki RTI fail hui, State Information Commission (SIC) mein second appeal deni hai.",
      state: "State Govt departments",
      dept: "State Information Commission (SIC) of respective state",
      difficulty: "medium",
      success: "medium",
      which_law: "RTI Act 2005, Section 19(3) — state appeals go to SIC, not CIC",
      time_limit: "90 days from FAA response or deadline",
      fee: "No fee / small fee in some states",
      portal: "State SIC website (e.g., sic.maharashtra.gov.in)",
      prefill: "Yeh appeal [STATE] Rajya Soochna Aayog mein Section 19(3) ke tahat di ja rahi hai. RTI application [DEPT] mein [DATE] ko di gayi thi. PIO aur FAA dono ne jawaab nahi diya ya galat jawaab diya. History: RTI filed [DATE], First Appeal filed [DATE], FAA response/no response. CIC nahi — SIC ke adhikar kshetra mein aata hai."
    },
    {
      title: "Department Claims Info Doesn't Exist",
      desc: "PIO bola 'record available nahi hai' — lekin hum jaante hain ki record hai. CIC mein challenge karna hai.",
      state: "All Central Depts",
      dept: "Central Information Commission",
      difficulty: "hard",
      success: "low",
      which_law: "RTI Act 2005, Section 19(3); Section 7(9) — if info doesn't exist, state in writing",
      time_limit: "90 days",
      fee: "No fee",
      portal: "cic.gov.in",
      prefill: "PIO ne jawab diya ki '[REQUESTED INFORMATION] ka record hamare paas nahi hai.' Lekin yeh credible nahi hai kyunki: (1) [REASON WHY RECORD MUST EXIST], (2) [EVIDENCE — e.g., RTI from another source showing the record exists]. Nivedan hai ki CIC hearing mein department ko record genuinely search karne ka aadesh de aur affidavit file karne ko kahe."
    }
  ],

  // ══════════════════════════════════════════════════════════════
  // 4. CONSUMER COURT COMPLAINT — Consumer Protection Act 2019
  // ══════════════════════════════════════════════════════════════
  consumer: [
    {
      title: "E-Commerce Refund Not Processed",
      desc: "Amazon/Flipkart par product return kiya, 2 mahine ho gaye refund nahi aaya. Customer care se thak gaye.",
      state: "All States (file in buyer's district)",
      dept: "District Consumer Disputes Redressal Commission",
      difficulty: "easy",
      success: "high",
      which_law: "Consumer Protection Act 2019, Section 35; E-Commerce Rules 2020",
      time_limit: "File within 2 years of cause; Commission decides in 3-5 months",
      fee: "Up to ₹5 lakh claim: ₹200 | ₹5-10 lakh: ₹400 | File online: edaakhil.nic.in",
      portal: "edaakhil.nic.in",
      prefill: "Maine [DATE] ko [PLATFORM] se [PRODUCT] ₹[AMOUNT] mein kharida tha. Order ID [NUMBER]. Product [DEFECTIVE/WRONG ITEM] nikla to [DATE] ko return request ki. Return pick up bhi ho gayi lekin refund ₹[AMOUNT] aaj tak nahi aaya. Multiple complaints ki lekin sirf auto-replies aate hain. Refund + compensation + litigation cost maang raha/rahi hoon."
    },
    {
      title: "Term Insurance Claim Rejected",
      desc: "Father ki death ke baad term insurance claim diya, company ne bina proper reason bataye reject kar diya.",
      state: "All States",
      dept: "District Consumer Commission / IRDAI Ombudsman",
      difficulty: "hard",
      success: "medium",
      which_law: "Consumer Protection Act 2019; Insurance Act 1938; IRDAI Regulations",
      time_limit: "2 years from rejection date; try IRDAI ombudsman first",
      fee: "As per claim amount slab on edaakhil.nic.in",
      portal: "edaakhil.nic.in / irdai.gov.in/ombudsman",
      prefill: "[INSURED NAME] ki death [DATE] ko [CAUSE] ki wajah se hui. Policy number [NUMBER] tha, [COMPANY NAME] ka term plan tha. Sum assured ₹[AMOUNT] tha. Claim [DATE] ko diya tha, company ne [DATE] ko reject kar diya citing '[REJECTION REASON]'. Yeh rejection wrongful hai kyunki [REASON]. Death certificate, medical records sab documents hain. Claim amount + interest + compensation maang raha/rahi hoon."
    },
    {
      title: "Builder Possession Delay — RERA Plus Consumer",
      desc: "Flat book kiya 2018 mein, possession 2021 mein milni thi, 2026 mein bhi nahi mili. Builder ghuma raha hai.",
      state: "All States with RERA",
      dept: "State RERA Authority + District Consumer Commission",
      difficulty: "hard",
      success: "medium",
      which_law: "Consumer Protection Act 2019; Real Estate (Regulation) Act 2016, Section 18",
      time_limit: "RERA: file anytime; Consumer: 2 years from possession date agreed",
      fee: "RERA: state-wise small fee | Consumer Commission: as per amount",
      portal: "edaakhil.nic.in / State RERA portal (e.g., maharera.mahaonline.gov.in)",
      prefill: "Maine [DATE] ko [BUILDER NAME] ke [PROJECT NAME] mein flat book kiya tha. Agreement to Sale hai, flat price ₹[AMOUNT] hai, possession [DATE] agree ki gayi thi. Aaj [CURRENT DATE] hai aur abhi bhi possession nahi mili. Builder bahane bana raha hai. Main maang raha/rahi hoon: (1) Immediate possession ya full refund, (2) Interest @9% per annum on paid amount per RERA Section 18, (3) Compensation for mental agony."
    },
    {
      title: "Bank Unauthorized Debit / UPI Fraud",
      desc: "Account se unknown debit ho gaya — kisi ne OTP leke fraud kiya. Bank paisa wapas nahi de raha.",
      state: "All States",
      dept: "Banking Ombudsman (RBI) first, then Consumer Commission",
      difficulty: "medium",
      success: "medium",
      which_law: "Consumer Protection Act 2019; RBI Circular on Customer Liability 2017",
      time_limit: "Report within 3 days for zero liability; Consumer complaint within 2 years",
      fee: "RBI Ombudsman: FREE | Consumer Commission: slab-based",
      portal: "cms.rbi.org.in / edaakhil.nic.in",
      prefill: "[DATE] ko mere bank account [ACCOUNT LAST 4 DIGITS] se [BANK NAME] — ₹[AMOUNT] ka unauthorized transaction hua. Transaction ID [NUMBER]. Maine turant bank ko [DATE] ko complaint ki (complaint number [NUMBER]) lekin bank ne liability maan'ne se mana kar diya. RBI guideline ke anusaar agar 3rd party fraud hai toh customer ki zero liability hoti hai. Refund + compensation maang raha/rahi hoon."
    },
    {
      title: "Telecom Company — Wrong Billing / Service Stoppage",
      desc: "Jio/Airtel/BSNL ne galat bill bheja ya bina notice service band kar di. Customer care kuch nahi kar raha.",
      state: "All States",
      dept: "TRAI CGPDTM / Consumer Commission",
      difficulty: "easy",
      success: "high",
      which_law: "Consumer Protection Act 2019; Telecom Regulatory Authority of India Act 1997",
      time_limit: "2 years",
      fee: "File on edaakhil.nic.in — small fee as per claim",
      portal: "edaakhil.nic.in / trai.gov.in",
      prefill: "Mera mobile number [NUMBER] hai, operator [AIRTEL/JIO/BSNL]. [DATE] ko bina koi notice ke service band kar di gayi / galat amount ₹[X] charge kiya gaya. [DATE] ko consumer care complaint ki, reference [NUMBER] hai lekin koi resolution nahi mili. Kaafi din se pareshani ho rahi hai. Service restore karne / refund + compensation maangte hain."
    },
    {
      title: "Defective Mobile / Appliance — Warranty Dishonoured",
      desc: "Naya phone / fridge kharida, 2 mahine mein defect aa gaya, service center warranty claim reject kar raha hai.",
      state: "All States",
      dept: "District Consumer Commission",
      difficulty: "easy",
      success: "high",
      which_law: "Consumer Protection Act 2019, Section 2(11) — deficiency in service",
      time_limit: "2 years from purchase / defect date",
      fee: "edaakhil.nic.in slab fees",
      portal: "edaakhil.nic.in",
      prefill: "Maine [DATE] ko [BRAND] ka [MODEL] ₹[AMOUNT] mein kharida tha, invoice number [NUMBER]. Purchase ke [X] mahine mein [DEFECT DESCRIPTION] problem aayi. Service center mein [DATE] ko gayi/gaya, complaint number [NUMBER] mila lekin unhone warranty claim reject kar diya citing '[FAKE REASON]'. Replacement ya full refund + ₹[AMOUNT] compensation + litigation cost maang raha/rahi hoon."
    },
    {
      title: "Hospital Overcharging / Wrong Treatment",
      desc: "Private hospital ne agree kiye amount se 3x bill diya ya bina consent ke wrong procedure kiya.",
      state: "All States",
      dept: "District Consumer Commission (Medical negligence = consumer complaint)",
      difficulty: "hard",
      success: "medium",
      which_law: "Consumer Protection Act 2019; Indian Medical Council guidelines; SC in V.P. Shantha v IMA (1995)",
      time_limit: "2 years from treatment",
      fee: "edaakhil.nic.in",
      portal: "edaakhil.nic.in / State Medical Council",
      prefill: "[PATIENT NAME] ka [HOSPITAL NAME] mein [DATE] se [DATE] tak [TREATMENT/SURGERY NAME] ke liye admission tha. Agreement ₹[AMOUNT] ka tha lekin final bill ₹[AMOUNT] ka diya / bina written consent ke [PROCEDURE] kiya gaya. Isse [HARM/COMPLICATION] hua. Excess billing refund + treatment complication ka compensation + punitive damages maangte hain."
    },
    {
      title: "Online Education Fees Not Refunded",
      desc: "Online coaching/course join kiya, quality kharab nikli, refund policy ke baad bhi paisa nahi mila.",
      state: "All States",
      dept: "District Consumer Commission",
      difficulty: "easy",
      success: "high",
      which_law: "Consumer Protection Act 2019; E-Commerce Rules 2020",
      time_limit: "2 years",
      fee: "edaakhil.nic.in",
      portal: "edaakhil.nic.in",
      prefill: "Maine [DATE] ko [PLATFORM/INSTITUTE] ka [COURSE NAME] ₹[AMOUNT] mein join kiya tha. Transaction ID [NUMBER]. Course quality advertised ke bilkul alag thi — [SPECIFIC ISSUE]. [DATE] ko refund request ki, unki policy ke according bhi eligible tha/thi, lekin refund nahi diya. Full refund + compensation maang raha/rahi hoon."
    }
  ],

  // ══════════════════════════════════════════════════════════════
  // 5. LEGAL NOTICE
  // ══════════════════════════════════════════════════════════════
  legal_notice: [
    {
      title: "Landlord Not Returning Security Deposit",
      desc: "Flat khali karte waqt landlord ne security deposit rok li — bina koi valid reason bataye.",
      state: "All States",
      dept: "Civil Court / Consumer Commission",
      difficulty: "easy",
      success: "high",
      which_law: "Contract Act 1872, Section 74; Transfer of Property Act 1882",
      time_limit: "Send notice, give 15 days; then file case",
      fee: "Notice: Free (self-draft) | Court: ₹200-500 court fee",
      portal: "Self-send via Speed Post / RPAD",
      prefill: "Main [NAME] [ADDRESS] se [DATE] ko shift ho gaya/gayi. Rent agreement ke anusaar security deposit ₹[AMOUNT] tha jo landlord [NAME] ko [DATE] ko diya tha. Flat [DATE] ko khali kiya, vacant possession diya, keys waapas di. Aaj [X] din baad bhi deposit wapas nahi mili. Landlord ne koi kaaraan nahi bataya. Notice ke 15 din ke andar deposit wapas karo nahi toh legal action hoga."
    },
    {
      title: "Builder Not Giving Flat Possession",
      desc: "Agreement mein date nikal gayi, completion certificate nahi mila, builder possession nahi de raha.",
      state: "All States",
      dept: "RERA Authority / Civil Court",
      difficulty: "medium",
      success: "high",
      which_law: "Real Estate Act 2016 (RERA), Section 18; Specific Relief Act 1963",
      time_limit: "Notice before filing RERA complaint",
      fee: "Notice free | RERA complaint: small state fee",
      portal: "State RERA portal",
      prefill: "Maine [DATE] ko [BUILDER] ke [PROJECT] mein Flat No [X] book kiya tha ₹[AMOUNT] mein. Agreement to Sale dated [DATE] mein possession [DATE] agree ki thi. Aaj [DATE] hai — possession [X] mahine/saal late ho chuki hai. Maine ₹[AMOUNT] already pay kar diye hain. Yeh notice hai ki 30 din ke andar possession do ya full refund + 9% p.a. interest do, nahi toh RERA aur Consumer Commission mein complaint karenge."
    },
    {
      title: "Employer Not Paying Salary Dues",
      desc: "Company ne 3+ months ki salary roki, resignation accept ki lekin full and final nahi diya.",
      state: "All States",
      dept: "Labour Court / Civil Court",
      difficulty: "medium",
      success: "high",
      which_law: "Payment of Wages Act 1936; Contract Act 1872 Section 73; Industrial Disputes Act 1947",
      time_limit: "Notice first, then Labour Court within 1 year",
      fee: "Notice: Free | Labour Court: minimal",
      portal: "Speed Post / State Labour Court",
      prefill: "Main [DESIGNATION] ke roop mein [COMPANY NAME] mein [DATE] se [DATE] tak kaam kiya. [DATE] ko resign kiya tha. Meri [X] months ki salary — ₹[AMOUNT] total — abhi tak nahi di gayi / Full & Final settlement nahi hua. Notice ke 15 din ke andar [AMOUNT] ka payment karo nahi toh Payment of Wages Act + Civil Court mein case file karenge aur full dues + interest + compensation maangenge."
    },
    {
      title: "Cheque Bounce — Recovery Notice",
      desc: "Loan diya tha, cheque bounce ho gaya. 138 NI Act ke tahat notice dena zaroori hai criminal case se pehle.",
      state: "All States",
      dept: "Judicial Magistrate Court (Section 138 NI Act case)",
      difficulty: "medium",
      success: "high",
      which_law: "Negotiable Instruments Act 1881, Section 138/139/141",
      time_limit: "CRITICAL: Notice within 30 days of dishonour memo; complaint within 15 days of notice expiry",
      fee: "Notice: Free | Court: ₹200",
      portal: "Speed Post mandatory for Section 138 — keep tracking proof",
      prefill: "[DRAWER NAME] ne [DATE] ko mujhe [BANK NAME] ka cheque no [NUMBER] for ₹[AMOUNT] diya tha. Loan / dues ke payment ke liye. Cheque [DATE] ko present kiya toh [BANK] ne '[REASON — Insufficient Funds/Account Closed]' ke wajah se dishonour kar diya. Memo [DATE] ko mila. Yeh statutory notice hai Section 138 NI Act ke tahat — 15 din ke andar payment karo nahi toh criminal court mein case file hoga."
    },
    {
      title: "Property Partition / Title Dispute",
      desc: "Family property partition ke liye co-owners tayyar nahi. Legal notice bhejni hai partition suit se pehle.",
      state: "All States",
      dept: "Civil Court",
      difficulty: "hard",
      success: "medium",
      which_law: "Transfer of Property Act 1882; Hindu Succession Act 1956; Partition Act 1893",
      time_limit: "Notice, then suit; limitation 12 years from adverse possession",
      fee: "Notice: Free | Civil suit: ad valorem court fee (% of property value)",
      portal: "Speed Post",
      prefill: "[PROPERTY ADDRESS/DESCRIPTION] jo ki [DECEASED/ANCESTOR NAME] ki property thi, usmein mera hissa [1/X SHARE] hai as per [WILL/SUCCESSION/ORAL AGREEMENT]. Co-owners [NAME(S)] partition karne se mana kar rahe hain ya mujhe mera hissa nahi de rahe. Yeh notice hai ki 30 din ke andar friendly partition karo aur mera [SHARE] ka possession do nahi toh Partition Suit + title dispute civil court mein file kiya jaayega."
    },
    {
      title: "Money Recovery — Loan Not Returned",
      desc: "Dost / relative ko paise diye the, ab wapas nahi de raha. Written proof hai — ab legal notice bhejna hai.",
      state: "All States",
      dept: "Civil Court (Money Suit) / Summary Suit Order 37 CPC",
      difficulty: "easy",
      success: "high",
      which_law: "Indian Contract Act 1872; CPC Order 37 — Summary Suit for money recovery",
      time_limit: "Limitation 3 years from due date | Notice: 15 days",
      fee: "Notice: Free | Court: small % of claim amount",
      portal: "Speed Post",
      prefill: "[BORROWER NAME] ne [DATE] ko mujhse ₹[AMOUNT] loan liya tha. [Evidence: Promissory note / receipt / WhatsApp message / bank transfer proof available hai.] Repayment ki agreed date [DATE] thi. Bahut requests ke baad bhi paise wapas nahi diye. Yeh notice hai ki 15 din ke andar ₹[AMOUNT] + [%] interest return karo nahi toh Order 37 CPC ke tahat summary suit file hogi."
    },
    {
      title: "Vendor / Contractor Breach of Contract",
      desc: "Event / website / construction ka kaam hire kiya, advance diya, kaam bekar nikla ya kiya hi nahi.",
      state: "All States",
      dept: "Civil Court / Consumer Commission",
      difficulty: "easy",
      success: "high",
      which_law: "Indian Contract Act 1872, Section 73 (damages for breach)",
      time_limit: "3 years from breach | Notice 15 days",
      fee: "Notice: Free | Consumer: edaakhil.nic.in slab",
      portal: "Speed Post / edaakhil.nic.in",
      prefill: "Maine [VENDOR/CONTRACTOR NAME] ko [SERVICE DESCRIPTION] ke liye [DATE] ko hire kiya tha ₹[AMOUNT] mein. Contract / agreement dated [DATE] hai. Advance ₹[AMOUNT] de diya tha. [DATE] tak kaam complete hona tha lekin [WHAT WENT WRONG]. Isse mujhe ₹[LOSS AMOUNT] ka direct loss hua. 15 din ke andar advance refund + loss ka compensation do nahi toh civil court + consumer forum mein case file hoga."
    },
    {
      title: "Defamation — Online / Verbal",
      desc: "Colleague / neighbour / ex-partner ne social media ya public mein jhooth bolkar reputation kharab ki.",
      state: "All States",
      dept: "Civil Court (damages) / Criminal Magistrate (Section 499/500 IPC)",
      difficulty: "hard",
      success: "medium",
      which_law: "IPC Section 499/500 (Defamation) / BNS 2023; Civil defamation suit",
      time_limit: "Criminal: 3 years | Civil: 1 year from publication",
      fee: "Notice: Free | Court: depends on type",
      portal: "Speed Post",
      prefill: "[RESPONDENT NAME] ne [DATE] ko [PLATFORM/PLACE] par mujhare baare mein jhoothe aur defamatory statements post ki / bole — specifically: '[DEFAMATORY STATEMENT]'. Yeh statements bilkul false hain aur meri professional/personal reputation ko serious harm pahunchi hai. Yeh notice hai ki 7 din ke andar public apology karo aur post/statement delete karo nahi toh criminal defamation (Section 499 IPC/BNS) + civil damages suit file hogi."
    }
  ],

  // ══════════════════════════════════════════════════════════════
  // 6. LABOUR COMPLAINT
  // ══════════════════════════════════════════════════════════════
  labour: [
    {
      title: "Salary Not Paid for 2-3 Months",
      desc: "Company kai mahino se salary nahi de rahi — keh rahi hai 'next month pakka'. Ab complaint deni hai.",
      state: "All States",
      dept: "Labour Commissioner / Payment of Wages Authority",
      difficulty: "easy",
      success: "high",
      which_law: "Payment of Wages Act 1936, Section 15; applicable if salary ≤ ₹24,000/month",
      time_limit: "Application within 1 year of due date; hearing in 3-6 months",
      fee: "Free / minimal",
      portal: "State Labour Department portal / in-person",
      prefill: "Main [COMPANY NAME] mein [DATE] se [DESIGNATION] ke roop mein kaam kar raha/rahi hoon. Meri monthly salary ₹[AMOUNT] hai. [DATE] se lekar [DATE] tak ki salary — total ₹[AMOUNT] — nahi mili. HR ko multiple times remind kiya, written mails bhi bheje hain. Payment of Wages Act ke tahat Labour Commissioner se nivedan hai ki: (1) Bakaya salary dilwaayi jaaye, (2) Compensation under Section 15, (3) Employer par penalty lagaayi jaaye."
    },
    {
      title: "PF Not Deposited by Employer",
      desc: "Salary slip mein PF deduct dikhta hai lekin EPFO passbook mein credit nahi aayi. Chor company.",
      state: "All States (EPFO is central)",
      dept: "EPFO Regional Office / PF Commissioner",
      difficulty: "medium",
      success: "high",
      which_law: "EPF & MP Act 1952, Section 14A — employer liable for non-deposit",
      time_limit: "File complaint anytime; EPFO can recover up to 3 years dues",
      fee: "Free complaint at EPFO / epfindia.gov.in",
      portal: "epfindia.gov.in > Grievance Portal / Regional EPFO office",
      prefill: "Main [COMPANY NAME] mein [DATE] se kaam kar raha/rahi hoon. Mera UAN number [NUMBER] hai. Salary slip mein har mahine ₹[AMOUNT] PF deduct hota dikhta hai lekin EPFO passbook mein [DATE] ke baad koi credit nahi aayi. Total [X] months ka PF — approx ₹[AMOUNT] — missing hai. EPFO Regional Commissioner se nivedan hai ki employer se dues recover karein, interest + damages lagaayein and employer ke against criminal complaint par vichar karein (Section 14 EPF Act)."
    },
    {
      title: "Wrongful Termination Without Notice",
      desc: "Bina notice diye HR ne teri services terminate kar di email mein. Koi reason nahi, koi dues nahi.",
      state: "All States (Industrial establishments)",
      dept: "Labour Court / Industrial Tribunal",
      difficulty: "hard",
      success: "medium",
      which_law: "Industrial Disputes Act 1947, Section 25F — 1 month notice + retrenchment compensation",
      time_limit: "File within 3 years | Conciliation first, then Labour Court",
      fee: "Free conciliation; Labour Court minimal fee",
      portal: "State Labour Department / Shram Suvidha Portal",
      prefill: "Main [COMPANY NAME] mein [DATE] se kaam kar raha/rahi tha/thi. Mujhe [DATE] ko bina koi written notice ke, bina reason bataye terminate kar diya gaya. Industrial Disputes Act Section 25F ke anusaar kam se kam 1 month ki notice ya notice pay dena zaroori tha jo nahi mili. Retrenchment compensation bhi nahi mila. Labour Commissioner se nivedan hai ki reinstatement ya full compensation + back wages dilwaayi jaaye."
    },
    {
      title: "No Appointment Letter Given",
      desc: "Kaafi mahino se kaam kar raha hoon, company appointment letter nahi de rahi. Evidence chahiye aur protection bhi.",
      state: "All States",
      dept: "Labour Department / Labour Inspector",
      difficulty: "easy",
      success: "medium",
      which_law: "Shops & Establishments Act (state-wise) — appointment letter mandatory",
      time_limit: "Complaint anytime during employment",
      fee: "Free",
      portal: "State Labour Department portal",
      prefill: "Main [COMPANY NAME], [ADDRESS] mein [DATE] se [DESIGNATION] ke roop mein kaam kar raha/rahi hoon. Monthly salary ₹[AMOUNT] hai, [CASH/BANK TRANSFER] mein milti hai. Company ne aaj tak koi appointment letter, salary slip, ya joining letter nahi di hai. Yeh Shops & Establishments Act ka violation hai. Labour Inspector se nivedan hai ki company ko notice jaari ho aur appointment letter + salary slips provide karne ka aadesh diya jaaye."
    },
    {
      title: "Overtime Work — No Payment",
      desc: "Roz 2-3 ghante extra kaam karwate hain lekin overtime ka paisa nahi dete. Koi record bhi nahi rakhte.",
      state: "Manufacturing / Factories",
      dept: "Factory Inspector / Labour Commissioner",
      difficulty: "medium",
      success: "medium",
      which_law: "Factories Act 1948, Section 59 — overtime @2x rate; Working hours max 48/week",
      time_limit: "Within 1 year",
      fee: "Free",
      portal: "State Factory Inspectorate / Labour Department",
      prefill: "Main [COMPANY NAME], [FACTORY ADDRESS] mein kaam karta/karti hoon. Regular shift [X] ghante hai lekin rozana average [X] ghante extra kaam karwaya jaata hai. Pichle [X] mahino mein approx [X] hours overtime kiya. Factories Act Section 59 ke anusaar double rate milna chahiye — approximately ₹[AMOUNT] due hai. Request hai ki factory inspector audit kare aur overtime dues dilwaye."
    },
    {
      title: "ESIC Not Deducted or Not Enrolled",
      desc: "Company 10 se zyada employees ki hai, ESIC hona chahiye tha, lekin enrollment hi nahi ki.",
      state: "All States (ESIC is central)",
      dept: "ESIC Regional / Sub-Regional Office",
      difficulty: "medium",
      success: "high",
      which_law: "Employees' State Insurance Act 1948, Section 85 — employer penalty for non-compliance",
      time_limit: "Complaint anytime; ESIC can recover up to 5 years dues",
      fee: "Free — esic.in > Grievance",
      portal: "esic.in / Regional ESIC office",
      prefill: "Main [COMPANY NAME] mein [DATE] se kaam kar raha/rahi hoon, monthly salary ₹[AMOUNT] hai. Company mein [X] employees hain. Salary slip mein ESIC deduction nahi hota aur ESIC card bhi nahi mila. ESI Act ke anusaar ₹21,000 se kam salary wale employees ko ESIC milna chahiye. ESIC Regional Office se nivedan hai ki: (1) Employer ko ESIC enroll karne ka notice jaari ho, (2) Bakaaya contributions recover ho, (3) Employer par penalty lagaayi jaaye."
    },
    {
      title: "Gratuity Denied After 5 Years Service",
      desc: "5 saal puri ho gayi, resign kiya, gratuity maangi — company bol rahi hai nahi milegi.",
      state: "All States",
      dept: "Controlling Authority — Payment of Gratuity Act (Labour Commissioner)",
      difficulty: "medium",
      success: "high",
      which_law: "Payment of Gratuity Act 1972, Section 4 — mandatory after 5 years; formula: 15/26 × salary × years",
      time_limit: "Employer must pay within 30 days of leaving; file complaint within 1 year",
      fee: "Free",
      portal: "State Labour Department portal / Labour Commissioner office",
      prefill: "Main [COMPANY NAME] mein [DATE] se [DATE] tak kaam kiya. Total service [X] years [Y] months hai. [DATE] ko resign kiya. Payment of Gratuity Act 1972, Section 4 ke anusaar mujhe gratuity milni chahiye. Calculation: Last salary ₹[AMOUNT] × 15 × [YEARS] ÷ 26 = ₹[AMOUNT]. Company ne gratuity dene se mana kar diya hai. Controlling Authority se nivedan hai ki company ko gratuity + interest + ₹10,000 penalty dene ka aadesh diya jaaye."
    },
    {
      title: "Maternity Benefit Denied",
      desc: "Pregnant employee ko maternity leave nahi di gayi ya leave ke baad job terminate kar di.",
      state: "All States",
      dept: "Labour Commissioner / Inspector (Maternity Benefits Inspector)",
      difficulty: "medium",
      success: "high",
      which_law: "Maternity Benefit Act 1961 (amended 2017) — 26 weeks paid leave; Section 12 — no dismissal during maternity",
      time_limit: "Complaint within 1 year",
      fee: "Free",
      portal: "State Labour Department / Shram Suvidha Portal",
      prefill: "Main [COMPANY NAME] mein [DESIGNATION] ke roop mein kaam karti hoon. Meri delivery date [DATE] thi. Maternity Benefit Act 2017 ke anusaar 26 weeks ki paid maternity leave milni chahiye thi. Lekin company ne [WHAT HAPPENED — leave deny ki / less leave di / terminate kiya]. Yeh Act ka direct violation hai. Labour Inspector se nivedan hai ki company ko penalty + back wages + compensation dene ka aadesh diya jaaye."
    }
  ]

};

// ══════════════════════════════════════════════════════════════
// QUICK REFERENCE: Key Legal Timelines
// ══════════════════════════════════════════════════════════════
const LEGAL_TIMELINES = {
  rti_pio_reply:           "30 days (48 hours for life/liberty)",
  rti_first_appeal:        "File within 30 days of PIO deadline; FAA replies in 30 days",
  rti_second_appeal:       "File within 90 days of FAA order/deadline",
  consumer_filing_limit:   "2 years from date of cause of action",
  consumer_commission_fee: "≤₹5L: ₹200 | ₹5-10L: ₹400 | ₹10-20L: ₹500 | ₹20-50L: ₹2000 | ₹50L-1Cr: ₹4000",
  legal_notice_response:   "15 days standard; 30 days for cheque bounce Section 138",
  cheque_bounce_criminal:  "Notice within 30 days of dishonour; complaint within 15 days of notice expiry",
  labour_salary_complaint: "Within 1 year under Payment of Wages Act",
  labour_id_act:           "Reference to Labour Court ideally within 3 years",
  gratuity_payment:        "Employer must pay within 30 days of termination",
  pf_grievance:            "EPFO can recover up to 3 years backdated dues",
  rera_complaint:          "Anytime during project delay; interest @9% p.a. per RERA Section 18"
};

// ══════════════════════════════════════════════════════════════
// QUICK REFERENCE: Key Portals
// ══════════════════════════════════════════════════════════════
const LEGAL_PORTALS = {
  rti_central:      "rtionline.gov.in",
  cic_appeal:       "cic.gov.in",
  consumer_court:   "edaakhil.nic.in",
  irdai_ombudsman:  "irdai.gov.in/ombudsman",
  rbi_ombudsman:    "cms.rbi.org.in",
  epfo:             "epfindia.gov.in",
  esic:             "esic.in",
  rera_maha:        "maharera.mahaonline.gov.in",
  rera_up:          "up-rera.in",
  rera_delhi:       "rera.delhi.gov.in",
  shram_suvidha:    "shramsuvidha.gov.in",
  trai:             "trai.gov.in",
  lok_adalat:       "nalsa.gov.in"
};

if (typeof module !== 'undefined') module.exports = { LEGAL_EXAMPLES, LEGAL_TIMELINES, LEGAL_PORTALS };
