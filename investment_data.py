"""
Nexora Global Investment & Business Migration Programs Database
Comprehensive worldwide investment programs and business migration opportunities
"""

investment_programs = {
    "USA": {
        "EB-5 Immigrant Investor Program": {
            "Documents": [
                "Passport: Valid for at least 6 months",
                "Form I-485: Application to Register Permanent Residence",
                "Form I-526: Immigrant Petition by Alien Entrepreneur",
                "Proof of funds: Investment capital of $1 million (or $500k in TEA areas)",
                "Business plan: Detailed investment project plan",
                "Financial documents: Bank statements, tax returns, proof of source of funds",
                "Employment verification: Letters showing job creation plan"
            ],
            "Investment Required": "$500,000 - $1,000,000",
            "Processing Time": "18-36 months",
            "Embassy Locations": ["New York", "Los Angeles", "Chicago", "Houston", "Miami"],
            "Interview Requirement": "Yes, interview required",
            "Benefits": "Permanent residency, family inclusion, path to citizenship",
            "Notes": "Investment must create at least 10 jobs. Regional centers available for easier processing."
        },
        "E-2 Treaty Investor Visa": {
            "Documents": [
                "Passport: Valid travel document",
                "DS-156: Nonimmigrant Visa Application",
                "Photos: Recent passport-style photos",
                "Business registration: Company formation documents",
                "Investment proof: Bank statements, evidence of capital transfer",
                "Business plan: Detailed operational and financial plan",
                "Tax returns: Previous 2-3 years",
                "Employment letters: Verification of business operations"
            ],
            "Investment Required": "$50,000 - $100,000 (minimum)",
            "Processing Time": "2-4 weeks",
            "Embassy Locations": ["Nationwide",
 "Treaty-dependent countries"],
            "Interview Requirement": "Yes, interview required",
            "Benefits": "Valid up to 5 years, renewable, can bring family",
            "Notes": "Available for nationals of 60+ treaty countries. Can manage any size business."
        },
        "EB-1C Multinational Executive": {
            "Documents": [
                "Form I-140: Immigrant Petition for Alien Worker",
                "Passport and travel documents",
                "Evidence of executive/manager status",
                "Organizational chart and company documents",
                "Tax returns: 3-5 years for both companies",
                "Employment verification: Letters from both employers",
                "Business relationship documentation"
            ],
            "Investment Required": "Business ownership transfer",
            "Processing Time": "12-24 months",
            "Embassy Locations": ["Major US cities"],
            "Interview Requirement": "Usually yes",
            "Benefits": "Green card for executive/manager, family eligibility",
            "Notes": "For managers/executives transferring between companies."
        }
    },
    "United Kingdom": {
        "Innovator Visa": {
            "Documents": [
                "Passport: Valid for duration of stay",
                "Business plan: Detailed 3-5 year plan",
                "Endorsement: From accredited body",
                "Financial documents: Proof of £50,000 investment",
                "CV and qualifications",
                "English language certificate: CEFR level B2 or above",
                "Tuberculosis test: If required"
            ],
            "Investment Required": "£50,000 minimum",
            "Processing Time": "8 weeks",
            "Embassy Locations": ["London", "Birmingham", "Manchester", "Edinburgh"],
            "Interview Requirement": "May be required",
            "Benefits": "Route to settlement, business ownership in UK",
            "Notes": "For founders of innovative businesses. Can bring spouse and dependents."
        },
        "Startup Visa": {
            "Documents": [
                "Passport",
                "Business plan",
                "Endorsement from accredited body",
                "CV and qualifications",
                "English language evidence",
                "Financial documents",
                "Tuberculosis certificate"
            ],
            "Investment Required": "No specific investment required",
            "Processing Time": "8 weeks",
            "Embassy Locations": ["Nationwide"],
            "Interview Requirement": "May be required",
            "Benefits": "Starting point for business, family can join",
            "Notes": "For early-stage entrepreneurs with innovative ideas."
        },
        "Standard Visitor Visa": {
            "Documents": [
                "Valid passport",
                "Completed application form",
                "Passport-style photo",
                "Proof of funds: £945 + living costs",
                "Proof of ties to home country",
                "Return flight booking"
            ],
            "Investment Required": "N/A (Visa cost £115)",
            "Processing Time": "3 weeks - 3 months",
            "Embassy Locations": ["Worldwide"],
            "Interview Requirement": "Usually not required",
            "Benefits": "Short-term business/tourism",
            "Notes": "Valid for 6 months. No work permitted."
        }
    },
    "Germany": {
        "Self-Employment Visa": {
            "Documents": [
                "Passport",
                "Business plan: Detailed plan in German/English",
                "Evidence of qualifications: Credentials, resume",
                "Financial proof: Sufficient capital (€50,000-€100,000)",
                "Insurance documents: Health insurance",
                "Tax registration certificate",
                "Lease agreement for business location"
            ],
            "Investment Required": "€50,000 - €100,000",
            "Processing Time": "6-8 weeks",
            "Embassy Locations": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
            "Interview Requirement": "Yes, usually required",
            "Benefits": "Path to permanent residency, family sponsorship",
            "Notes": "For entrepreneurs setting up business in Germany."
        },
        "EU Blue Card": {
            "Documents": [
                "Passport",
                "Employment contract",
                "Degree certificate: Relevant qualification",
                "Health insurance",
                "Proof of funds for living"
            ],
            "Investment Required": "N/A (Employment-based)",
            "Processing Time": "4-6 weeks",
            "Embassy Locations": ["Major cities"],
            "Interview Requirement": "Usually not required",
            "Benefits": "EU mobility, family reunification possible",
            "Notes": "For highly skilled workers earning €55,200+ annually."
        }
    },
    "Singapore": {
        "EntrePass": {
            "Documents": [
                "Passport",
                "Business registration documents",
                "Shareholders' agreement",
                "Company's financial statements",
                "Business plan: Detailed operations plan",
                "Personal financial documents",
                "Educational/professional credentials"
            ],
            "Investment Required": "SGD 500,000 (preferred) or business acumen",
            "Processing Time": "4-6 weeks",
            "Embassy Locations": ["Singapore"],
            "Interview Requirement": "May be required",
            "Benefits": "Self-employment, path to permanent residency",
            "Notes": "For foreign entrepreneurs starting business in Singapore."
        },
        "Tech.Pass": {
            "Documents": [
                "Passport",
                "Resume/CV",
                "Job offer letter",
                "Company incorporation certificate",
                "Educational qualifications"
            ],
            "Investment Required": "N/A (Employment-based)",
            "Processing Time": "2-3 weeks",
            "Embassy Locations": ["Singapore"],
            "Interview Requirement": "Usually not required",
            "Benefits": "Tech talent fast-track, family eligible",
            "Notes": "For tech professionals earning SGD 14,000+ monthly."
        }
    },
    "Canada": {
        "Start-up Visa": {
            "Documents": [
                "Passport",
                "Business plan",
                "Letter of support from designated organization",
                "Proof of funds: CAD 75,000+",
                "Educational credentials",
                "Language test: IELTS or TOEFL",
                "Medical exam results"
            ],
            "Investment Required": "CAD 75,000+",
            "Processing Time": "12-16 months",
            "Embassy Locations": ["Toronto", "Vancouver", "Calgary", "Montreal"],
            "Interview Requirement": "May be required",
            "Benefits": "Path to permanent residency, family eligibility",
            "Notes": "For innovative entrepreneurs with backing from Canadian investors."
        },
        "Self-Employed": {
            "Documents": [
                "Passport",
                "Proof of experience: 2 years in past 5 years",
                "Financial proof: CAD 20,000+",
                "Language test scores",
                "Education credentials",
                "Medical and police certificates"
            ],
            "Investment Required": "CAD 20,000+",
            "Processing Time": "12-24 months",
            "Embassy Locations": ["Nationwide"],
            "Interview Requirement": "Likely",
            "Benefits": "Permanent residency, family can join",
            "Notes": "For individuals who are self-employed in an eligible occupation."
        }
    },
    "Australia": {
        "Skilled Visa (189)": {
            "Documents": [
                "Passport",
                "Skills assessment: From accredited body",
                "English language test: IELTS",
                "Educational credentials",
                "Work experience documentation",
                "Medical and police certificates",
                "State sponsorship (if applicable)"
            ],
            "Investment Required": "N/A (Points-based)",
            "Processing Time": "8-16 weeks",
            "Embassy Locations": ["Sydney", "Melbourne", "Brisbane", "Perth"],
            "Interview Requirement": "Usually not required",
            "Benefits": "Permanent residency, skilled worker status",
            "Notes": "Points-based system. Requires 65 points minimum."
        },
        "Business Innovation Visa (188A)": {
            "Documents": [
                "Passport",
                "Business plan",
                "Financial records: 2-3 years",
                "Evidence of investment capital",
                "English language certificate",
                "Medical and police checks",
                "State nomination"
            ],
            "Investment Required": "AUD 200,000 - AUD 1,250,000",
            "Processing Time": "12-24 months",
            "Embassy Locations": ["Major cities"],
            "Interview Requirement": "Usually yes",
            "Benefits": "Provisional residency, path to permanent residency",
            "Notes": "For business owners/investors. Can lead to 888 subclass."
        }
    },
    "Portugal": {
        "Golden Visa (Investment)": {
            "Documents": [
                "Passport",
                "Investment proof: €280,000+ (or other eligible investment)",
                "Financial documents: Bank statements, tax returns",
                "Business plan",
                "Police certificate",
                "Medical certificate",
                "Proof of accommodation"
            ],
            "Investment Required": "€280,000 - €500,000+",
            "Processing Time": "60-90 days",
            "Embassy Locations": ["Lisbon", "Porto"],
            "Interview Requirement": "Usually not required",
            "Benefits": "Residency, path to citizenship after 5 years",
            "Notes": "Multiple investment options including real estate, business, and employment creation."
        },
        "Digital Nomad Visa": {
            "Documents": [
                "Passport",
                "Employment contract or business registration",
                "Proof of income: €2,700+ monthly",
                "Health insurance",
                "Proof of accommodation",
                "Criminal record check"
            ],
            "Investment Required": "N/A (Income requirement €2,700/month)",
            "Processing Time": "4-6 weeks",
            "Embassy Locations": ["Worldwide"],
            "Interview Requirement": "Usually not required",
            "Benefits": "1-year residency, renewable, work from Portugal",
            "Notes": "For remote workers and freelancers."
        }
    },
    "Dubai (UAE)": {
        "Investor Visa": {
            "Documents": [
                "Passport",
                "Proof of investment: AED 500,000+",
                "Real estate purchase agreement (if applicable)",
                "Financial statements",
                "Business documents",
                "Medical test: Results",
                "Emirates ID application"
            ],
            "Investment Required": "AED 500,000 - AED 1,000,000+",
            "Processing Time": "2-4 weeks",
            "Embassy Locations": ["Dubai", "Abu Dhabi", "Sharjah"],
            "Interview Requirement": "Rarely",
            "Benefits": "Long-term residency, fast-track, family eligible",
            "Notes": "3-year renewable visa. Can invest in real estate or business."
        },
        "Business License Visa": {
            "Documents": [
                "Passport",
                "Business plan",
                "Commercial registration",
                "Lease agreement",
                "Financial proof",
                "Medical examination",
                "Background check"
            ],
            "Investment Required": "AED 100,000+ (variable by sector)",
            "Processing Time": "1-2 weeks",
            "Embassy Locations": ["Major emirates"],
            "Interview Requirement": "Usually not required",
            "Benefits": "Business ownership, residency, family sponsorship",
            "Notes": "Flexible business setup options available."
        }
    },
    "Switzerland": {
        "Entrepreneur Visa": {
            "Documents": [
                "Passport",
                "Business plan: Detailed CHF",
                "Financial proof: CHF 50,000+",
                "Company registration: Copy",
                "Lease agreement: Proof of location",
                "Educational documents",
                "Insurance: Health insurance"
            ],
            "Investment Required": "CHF 50,000 - CHF 200,000",
            "Processing Time": "8-12 weeks",
            "Embassy Locations": ["Bern", "Zurich", "Geneva", "Basel"],
            "Interview Requirement": "Yes, usually required",
            "Benefits": "Business residency, family can join",
            "Notes": "Approved by cantonal government. Must contribute to employment."
        }
    }
}

company_info = {
    "name": "Aidni Global LLP",
    "headquarters": "Mumbai, India",
    "phone": "+919825728291",
    "email": "info@aidniglobal.com",
    "website": "www.aidniglobal.com",
    "expertise": "Global Investment & Business Migration Solutions"
}

def get_investment_info(country, program_type):
    """Retrieve investment program information by country and type"""
    if country in investment_programs:
        if program_type in investment_programs[country]:
            return investment_programs[country][program_type]
    return None

def get_all_countries():
    """Get list of all countries with investment programs"""
    return list(investment_programs.keys())

def get_programs_by_country(country):
    """Get all programs for a specific country"""
    if country in investment_programs:
        return list(investment_programs[country].keys())
    return []

def get_investment_requirement(country, program):
    """Get minimum investment required for a program"""
    try:
        return investment_programs[country][program].get("Investment Required", "N/A")
    except KeyError:
        return "N/A"

def get_processing_time(country, program):
    """Get processing time for a program"""
    try:
        return investment_programs[country][program].get("Processing Time", "N/A")
    except KeyError:
        return "N/A"
