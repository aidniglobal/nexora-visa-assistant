"""
Nexora Global Residency Programs Database
Comprehensive worldwide residency and visa programs database
Updated to match residencies.io and passports.io coverage
"""

residency_programs = {
    "Portugal": {
        "Golden Visa (Investment)": {
            "description": "Portugal's Golden Visa program offers residency and eventual citizenship through various investment options. The program is one of Europe's most popular, attracting global investors seeking EU residency.",
            "residency_type": "Investment",
            "country_info": {
                "capital": "Lisbon",
                "region": "Southern Europe",
                "language": "Portuguese",
                "currency": "EUR (€)",
                "eu_member": True,
                "schengen_member": True,
                "cost_of_living": "Moderate",
                "tax_rate": "15-48%"
            },
            "investment_types": {
                "Real Estate": {
                    "minimum": "€280,000",
                    "description": "Purchase of residential property",
                    "roi_potential": "Moderate (Property appreciation)"
                },
                "Business": {
                    "minimum": "€500,000",
                    "description": "Business investment and job creation",
                    "roi_potential": "High (Business growth)"
                },
                "Capital Transfer": {
                    "minimum": "€1,000,000",
                    "description": "Direct capital investment",
                    "roi_potential": "Variable"
                }
            },
            "processing_time": "60-120 days",
            "initial_permit_duration": "1 year (renewable)",
            "path_to_citizenship": "5 years",
            "visa_free_countries": 188,
            "family_members_eligible": True,
            "requirements": [
                "Valid passport",
                "Investment capital proof",
                "Health insurance",
                "Background checks",
                "Clean criminal record"
            ],
            "benefits": [
                "Residency in EU",
                "Schengen area travel",
                "Path to EU citizenship",
                "Family reunification",
                "Access to healthcare and education"
            ],
            "documents_required": [
                "Passport copy",
                "Bank statements",
                "Investment proposal",
                "Proof of funds",
                "Health insurance certificate"
            ],
            "cost": {
                "visa_fee": "€500",
                "administrative": "€250-500",
                "legal_consultation": "€1,000-3,000"
            },
            "application_steps": 4,
            "popular": True
        },
        "D7 Visa (Passive Income)": {
            "description": "For retirees and individuals with passive income",
            "residency_type": "Retirement/Passive Income",
            "monthly_income_required": "€1,200",
            "processing_time": "30-45 days",
            "initial_permit_duration": "1 year",
            "path_to_citizenship": "5 years",
            "visa_free_countries": 188,
            "family_members_eligible": True,
            "requirements": [
                "Proof of passive income (pensions, investments)",
                "Health insurance",
                "Accommodation proof",
                "Background checks"
            ],
            "benefits": [
                "Affordable living cost",
                "Healthcare access",
                "Flexible working rules",
                "EU residency"
            ],
            "documents_required": [
                "Passport",
                "Bank statements",
                "Pension documents",
                "Health insurance",
                "Lease agreement"
            ],
            "cost": {
                "visa_fee": "€100",
                "administrative": "€100-200"
            },
            "application_steps": 3,
            "popular": True
        }
    },
    "Malta": {
        "Residency and Visa Program": {
            "description": "EU country offering residency permits through investment. Malta is a strategic location for digital nomads and investors, combining EU membership with favorable tax policies.",
            "residency_type": "Investment",
            "country_info": {
                "capital": "Valletta",
                "region": "Southern Europe (Mediterranean)",
                "language": "Maltese, English",
                "currency": "EUR (€)",
                "eu_member": True,
                "schengen_member": True,
                "cost_of_living": "Moderate",
                "tax_rate": "0-35%",
                "digital_nomad_friendly": True
            },
            "investment_types": {
                "Real Estate Rental": {
                    "minimum": "€12,000/year",
                    "description": "Rental of property for 5 years",
                    "roi_potential": "Moderate"
                },
                "Purchase": {
                    "minimum": "€220,000",
                    "description": "Property purchase",
                    "roi_potential": "Moderate-High"
                },
                "Government Loan": {
                    "minimum": "€250,000",
                    "description": "Interest-free loan",
                    "roi_potential": "Low risk"
                }
            },
            "processing_time": "45-60 days",
            "initial_permit_duration": "5 years",
            "path_to_citizenship": "6 years total",
            "visa_free_countries": 188,
            "family_members_eligible": True,
            "requirements": [
                "Proof of funds",
                "Background checks",
                "Health insurance",
                "Employment or income proof"
            ],
            "benefits": [
                "EU residency",
                "Schengen access",
                "Low tax rates",
                "Mediterranean lifestyle",
                "Financial hub access"
            ],
            "documents_required": [
                "Passport",
                "Bank statements",
                "Property documents",
                "Financial records",
                "Tax returns"
            ],
            "cost": {
                "processing_fee": "€500",
                "administrative": "€300-1,000"
            },
            "application_steps": 4,
            "popular": True
        }
    },
    "Greece": {
        "Golden Visa": {
            "description": "Residency through real estate investment",
            "residency_type": "Investment",
            "investment_types": {
                "Real Estate": {
                    "minimum": "€250,000",
                    "description": "Property purchase",
                    "roi_potential": "Moderate"
                }
            },
            "processing_time": "60-90 days",
            "initial_permit_duration": "5 years (renewable)",
            "path_to_citizenship": "7 years",
            "visa_free_countries": 188,
            "family_members_eligible": True,
            "requirements": [
                "Investment in Greek property",
                "Clean background",
                "Health insurance",
                "Valid passport"
            ],
            "benefits": [
                "EU residency",
                "Lifetime renewable permit",
                "Family sponsorship",
                "Schengen travel"
            ],
            "documents_required": [
                "Passport",
                "Property deed",
                "Bank statements",
                "Health insurance"
            ],
            "cost": {
                "visa_fee": "€0",
                "administrative": "€500-1,000"
            },
            "application_steps": 3,
            "popular": True
        }
    },
    "Spain": {
        "Golden Visa": {
            "description": "Residency through property investment or business",
            "residency_type": "Investment",
            "investment_types": {
                "Real Estate": {
                    "minimum": "€500,000",
                    "description": "Property purchase",
                    "roi_potential": "Moderate-High"
                },
                "Business": {
                    "minimum": "€600,000",
                    "description": "Business investment",
                    "roi_potential": "High"
                }
            },
            "processing_time": "30-60 days",
            "initial_permit_duration": "1 year (renewable)",
            "path_to_citizenship": "5-10 years",
            "visa_free_countries": 188,
            "family_members_eligible": True,
            "requirements": [
                "Investment proof",
                "Income of €2,000/month",
                "Health insurance",
                "Clean record"
            ],
            "benefits": [
                "EU access",
                "Family reunification",
                "Work authorization",
                "Healthcare system access"
            ],
            "documents_required": [
                "Passport",
                "Investment documents",
                "Bank statements",
                "Health insurance",
                "Tax certificate"
            ],
            "cost": {
                "visa_fee": "€100",
                "administrative": "€300-500"
            },
            "application_steps": 4,
            "popular": True
        }
    },
    "Cyprus": {
        "Permanent Residence Permit": {
            "description": "Residency through property and financial investment",
            "residency_type": "Investment",
            "investment_types": {
                "Real Estate": {
                    "minimum": "€200,000",
                    "description": "Property purchase",
                    "roi_potential": "Moderate"
                },
                "Savings": {
                    "minimum": "€50,000",
                    "description": "Bank deposit",
                    "roi_potential": "Low"
                }
            },
            "processing_time": "45-60 days",
            "initial_permit_duration": "Permanent",
            "path_to_citizenship": "8-15 years",
            "visa_free_countries": 188,
            "family_members_eligible": True,
            "requirements": [
                "Property ownership or rental proof",
                "Income €2,000/month minimum",
                "Health insurance",
                "Clean background"
            ],
            "benefits": [
                "Permanent residency",
                "EU access",
                "Tax benefits",
                "Dual residency possible"
            ],
            "documents_required": [
                "Passport",
                "Property deed",
                "Bank statements",
                "Insurance certificate"
            ],
            "cost": {
                "visa_fee": "€0",
                "processing": "€500-1,000"
            },
            "application_steps": 3,
            "popular": True
        }
    },
    "United Kingdom": {
        "Tier 1 Investor Visa": {
            "description": "Residency through business investment",
            "residency_type": "Investment",
            "investment_types": {
                "Business Investment": {
                    "minimum": "£2,000,000",
                    "description": "Investment in UK business",
                    "roi_potential": "High"
                },
                "Startup": {
                    "minimum": "£50,000",
                    "description": "Business startup",
                    "roi_potential": "Variable"
                }
            },
            "processing_time": "90-120 days",
            "initial_permit_duration": "3 years",
            "path_to_citizenship": "5 years",
            "visa_free_countries": 187,
            "family_members_eligible": True,
            "requirements": [
                "Capital investment proof",
                "Business plan",
                "Sponsor approval",
                "English proficiency"
            ],
            "benefits": [
                "UK residency",
                "Path to citizenship",
                "Work authorization",
                "Family sponsorship"
            ],
            "documents_required": [
                "Passport",
                "Bank statements",
                "Business documents",
                "Tax returns",
                "Sponsor certificate"
            ],
            "cost": {
                "visa_fee": "£1,033",
                "processing": "£2,000-5,000"
            },
            "application_steps": 4,
            "popular": True
        },
        "Skilled Worker Visa": {
            "description": "Employment-based residency",
            "residency_type": "Employment",
            "minimum_salary": "£26,200",
            "processing_time": "60-90 days",
            "initial_permit_duration": "5 years",
            "path_to_citizenship": "6 years total",
            "visa_free_countries": 187,
            "family_members_eligible": True,
            "requirements": [
                "Job offer from UK sponsor",
                "English proficiency",
                "Health insurance"
            ],
            "benefits": [
                "UK residency",
                "Family reunification",
                "Healthcare access",
                "Path to citizenship"
            ],
            "documents_required": [
                "Passport",
                "Job offer letter",
                "Qualification certificates",
                "Health insurance"
            ],
            "cost": {
                "visa_fee": "£719",
                "processing": "£500-1,500"
            },
            "application_steps": 3,
            "popular": False
        }
    },
    "Canada": {
        "Entrepreneur Immigration Program": {
            "description": "Business immigration program",
            "residency_type": "Business/Investment",
            "investment_types": {
                "Business": {
                    "minimum": "CAD $300,000",
                    "description": "Business establishment",
                    "roi_potential": "High"
                }
            },
            "processing_time": "24 months",
            "initial_permit_duration": "3 years (renewable)",
            "path_to_citizenship": "3 years as permanent resident",
            "visa_free_countries": 189,
            "family_members_eligible": True,
            "requirements": [
                "Business plan",
                "Capital investment",
                "Management experience",
                "Language proficiency"
            ],
            "benefits": [
                "Permanent residency path",
                "Family sponsorship",
                "Healthcare and education",
                "Eventually citizenship"
            ],
            "documents_required": [
                "Passport",
                "Business plan",
                "Financial documents",
                "Language test",
                "Job creation plan"
            ],
            "cost": {
                "application_fee": "CAD $2,500",
                "processing": "CAD $1,000-3,000"
            },
            "application_steps": 5,
            "popular": True
        },
        "Express Entry": {
            "description": "Fast-track immigration for skilled workers",
            "residency_type": "Employment",
            "processing_time": "6 months",
            "initial_permit_duration": "3 years (can extend)",
            "path_to_citizenship": "3 years as permanent resident",
            "visa_free_countries": 189,
            "family_members_eligible": True,
            "requirements": [
                "Language proficiency",
                "Education credentials",
                "Work experience",
                "High CRS score"
            ],
            "benefits": [
                "Permanent residency",
                "Work authorization",
                "Family sponsorship",
                "Healthcare and education"
            ],
            "documents_required": [
                "Passport",
                "Language test results",
                "Education credentials",
                "Work experience letters"
            ],
            "cost": {
                "application_fee": "CAD $825",
                "processing": "Minimal additional"
            },
            "application_steps": 3,
            "popular": True
        }
    },
    "Australia": {
        "Skilled Independent Visa": {
            "description": "For skilled workers in demand occupations",
            "residency_type": "Skilled Migration",
            "processing_time": "12-24 months",
            "initial_permit_duration": "Permanent residency",
            "path_to_citizenship": "4 years",
            "visa_free_countries": 187,
            "family_members_eligible": True,
            "requirements": [
                "Occupation on skilled list",
                "Points score minimum",
                "Language proficiency",
                "Health and character checks"
            ],
            "benefits": [
                "Permanent residency",
                "Work anywhere in Australia",
                "Study benefits",
                "Family sponsorship"
            ],
            "documents_required": [
                "Passport",
                "Skills assessment",
                "Language test",
                "Work experience letters",
                "Educational credentials"
            ],
            "cost": {
                "visa_fee": "AUD $3,865",
                "assessment": "AUD $500-2,000"
            },
            "application_steps": 4,
            "popular": True
        },
        "Investor Visa": {
            "description": "Business and investment immigration",
            "residency_type": "Investment",
            "investment_types": {
                "Significant Business": {
                    "minimum": "AUD $1,500,000",
                    "description": "Significant investment in business",
                    "roi_potential": "High"
                },
                "Premium Investment": {
                    "minimum": "AUD $5,000,000",
                    "description": "Major investment",
                    "roi_potential": "High"
                }
            },
            "processing_time": "12-24 months",
            "initial_permit_duration": "4 years",
            "path_to_citizenship": "4 years additional",
            "visa_free_countries": 187,
            "family_members_eligible": True,
            "requirements": [
                "Capital investment",
                "Business plan",
                "English proficiency",
                "Health checks"
            ],
            "benefits": [
                "Permanent residency pathway",
                "Business operation freedom",
                "Family sponsorship",
                "Medicare access"
            ],
            "documents_required": [
                "Passport",
                "Business plan",
                "Financial statements",
                "Investment proof",
                "Tax returns"
            ],
            "cost": {
                "visa_fee": "AUD $4,765",
                "processing": "AUD $2,000-5,000"
            },
            "application_steps": 4,
            "popular": False
        }
    },
    "UAE": {
        "Golden Visa": {
            "description": "Long-term residency for investors and professionals",
            "residency_type": "Investment/Employment",
            "investment_types": {
                "Real Estate": {
                    "minimum": "AED 750,000",
                    "description": "Property purchase",
                    "roi_potential": "Moderate"
                },
                "Business": {
                    "minimum": "Varies",
                    "description": "Business establishment",
                    "roi_potential": "High"
                }
            },
            "processing_time": "30-45 days",
            "initial_permit_duration": "10 years",
            "path_to_citizenship": "No citizenship path",
            "visa_free_countries": 183,
            "family_members_eligible": True,
            "requirements": [
                "Investment or employment",
                "Clean background",
                "Valid passport",
                "Financial stability"
            ],
            "benefits": [
                "10-year residency",
                "Family sponsorship",
                "Business ownership",
                "Healthcare access"
            ],
            "documents_required": [
                "Passport",
                "Property deed or business license",
                "Financial statements",
                "Employment letter",
                "Medical records"
            ],
            "cost": {
                "visa_fee": "AED 0",
                "processing": "AED 500-2,000"
            },
            "application_steps": 3,
            "popular": True
        }
    },
    "Singapore": {
        "Tech.Pass Program": {
            "description": "For tech experts and professionals",
            "residency_type": "Employment/Tech",
            "minimum_salary": "SGD $30,000/month",
            "processing_time": "2-4 weeks",
            "initial_permit_duration": "3 years",
            "path_to_citizenship": "5+ years",
            "visa_free_countries": 189,
            "family_members_eligible": True,
            "requirements": [
                "Tech company employment",
                "Minimum salary threshold",
                "Educational background",
                "Employment contract"
            ],
            "benefits": [
                "Fast processing",
                "3-year permit",
                "Work authorization",
                "Family benefits"
            ],
            "documents_required": [
                "Passport",
                "Employment contract",
                "Educational certificates",
                "Bank statements"
            ],
            "cost": {
                "visa_fee": "SGD $240",
                "processing": "Minimal"
            },
            "application_steps": 2,
            "popular": True
        }
    }
}

def get_residency_info(country, program_type):
    """Get residency information for a specific country and program"""
    if country in residency_programs:
        if program_type in residency_programs[country]:
            return residency_programs[country][program_type]
    return None

def get_all_countries():
    """Get list of all countries with residency programs"""
    return list(residency_programs.keys())

def get_programs_by_country(country):
    """Get all programs available in a country"""
    if country in residency_programs:
        return list(residency_programs[country].keys())
    return []

def filter_programs(filters):
    """
    Filter residency programs by criteria
    filters: {
        'residency_type': 'Investment',
        'max_investment': 500000,
        'min_processing_time': 60,
        'citizenship_path': True
    }
    """
    results = []
    for country, programs in residency_programs.items():
        for program_name, program_data in programs.items():
            match = True
            
            if 'residency_type' in filters:
                if program_data.get('residency_type') != filters['residency_type']:
                    match = False
            
            if match and 'max_investment' in filters and 'investment_types' in program_data:
                found_match = False
                for inv_type, inv_data in program_data['investment_types'].items():
                    min_amount = int(inv_data['minimum'].replace('€', '').replace('£', '').replace('CAD $', '').replace('AUD $', '').replace('AED ', '').replace('SGD $', '').replace('/year', '').replace(',', ''))
                    if min_amount <= filters['max_investment']:
                        found_match = True
                        break
                if not found_match:
                    match = False
            
            if match and 'citizenship_available' in filters:
                has_citizenship = program_data.get('path_to_citizenship', '').lower() != 'no citizenship path'
                if filters['citizenship_available'] != has_citizenship:
                    match = False
            
            if match:
                results.append({
                    'country': country,
                    'program': program_name,
                    'data': program_data
                })
    
    return results
