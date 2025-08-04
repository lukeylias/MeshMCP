"""
Placeholder data generation for insurance/healthcare context
Generates realistic Australian insurance data for prototyping
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from faker import Faker
from faker.providers import BaseProvider

# Create Faker instance with Australian locale
fake = Faker('en_AU')

class InsuranceProvider(BaseProvider):
    """Custom provider for insurance-specific data"""
    
    # Australian insurance-specific data
    policy_types = [
        'Hospital Cover', 'Extras Cover', 'Hospital + Extras',
        'Basic Hospital', 'Bronze Hospital', 'Silver Hospital', 'Gold Hospital'
    ]
    
    policy_categories = ['Basic', 'Bronze', 'Silver', 'Gold', 'Platinum']
    
    claim_types = [
        'General Treatment', 'Major Dental', 'Optical', 'Physiotherapy',
        'Hospital Accommodation', 'Surgery', 'Specialist Consultation',
        'Pathology', 'Radiology', 'Emergency Department'
    ]
    
    claim_statuses = [
        'Submitted', 'Under Review', 'Approved', 'Paid', 'Rejected',
        'Pending Information', 'Processing', 'Completed'
    ]
    
    provider_types = [
        'General Practitioner', 'Specialist', 'Dentist', 'Physiotherapist',
        'Optometrist', 'Chiropractor', 'Psychologist', 'Hospital',
        'Pathology Lab', 'Radiology Clinic'
    ]
    
    australian_states = ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']
    
    def policy_type(self):
        return self.random_element(self.policy_types)
    
    def policy_category(self):
        return self.random_element(self.policy_categories)
    
    def claim_type(self):
        return self.random_element(self.claim_types)
    
    def claim_status(self):
        return self.random_element(self.claim_statuses)
    
    def provider_type(self):
        return self.random_element(self.provider_types)
    
    def australian_state(self):
        return self.random_element(self.australian_states)
    
    def policy_number(self):
        return f"POL{self.random_int(100000, 999999)}"
    
    def claim_number(self):
        return f"CLM{self.random_int(100000, 999999)}"
    
    def provider_number(self):
        return f"PRV{self.random_int(10000, 99999)}"
    
    def premium_amount(self):
        """Generate realistic premium amounts in AUD"""
        base_amounts = [89, 119, 159, 199, 249, 299, 359, 449, 599, 799]
        return random.choice(base_amounts) + random.randint(0, 50)
    
    def excess_amount(self):
        """Generate realistic excess amounts"""
        return random.choice([0, 250, 500, 750, 1000])

# Add the custom provider to faker
fake.add_provider(InsuranceProvider)

class DataGenerator:
    """Generate realistic placeholder data for insurance/healthcare context"""
    
    def __init__(self):
        self.fake = fake
    
    def generate_members(self, count: int = 10) -> List[Dict[str, Any]]:
        """Generate realistic member data"""
        members = []
        
        for _ in range(count):
            join_date = self.fake.date_between(start_date='-5y', end_date='today')
            
            member = {
                'id': self.fake.random_int(100000, 999999),
                'memberNumber': f"MBR{self.fake.random_int(100000, 999999)}",
                'firstName': self.fake.first_name(),
                'lastName': self.fake.last_name(),
                'email': self.fake.email(),
                'phone': self.fake.phone_number(),
                'dateOfBirth': self.fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
                'address': {
                    'street': self.fake.street_address(),
                    'suburb': self.fake.city(),
                    'state': self.fake.australian_state(),
                    'postcode': self.fake.postcode()
                },
                'joinDate': join_date.isoformat(),
                'status': random.choice(['Active', 'Suspended', 'Pending', 'Cancelled']),
                'policyType': self.fake.policy_type(),
                'policyCategory': self.fake.policy_category(),
                'monthlyPremium': self.fake.premium_amount(),
                'excess': self.fake.excess_amount(),
                'dependents': random.randint(0, 4),
                'lastPaymentDate': (join_date + timedelta(days=random.randint(0, 365))).isoformat(),
                'totalClaimsYTD': round(random.uniform(0, 5000), 2),
                'memberSince': f"{(datetime.now() - join_date).days // 365} years"
            }
            members.append(member)
        
        return members
    
    def generate_policies(self, count: int = 10) -> List[Dict[str, Any]]:
        """Generate realistic policy data"""
        policies = []
        
        for _ in range(count):
            start_date = self.fake.date_between(start_date='-3y', end_date='today')
            renewal_date = start_date + timedelta(days=365)
            
            policy = {
                'id': self.fake.random_int(100000, 999999),
                'policyNumber': self.fake.policy_number(),
                'memberNumber': f"MBR{self.fake.random_int(100000, 999999)}",
                'policyType': self.fake.policy_type(),
                'category': self.fake.policy_category(),
                'status': random.choice(['Active', 'Expired', 'Suspended', 'Cancelled']),
                'startDate': start_date.isoformat(),
                'renewalDate': renewal_date.isoformat(),
                'monthlyPremium': self.fake.premium_amount(),
                'annualPremium': self.fake.premium_amount() * 12,
                'excess': self.fake.excess_amount(),
                'benefits': {
                    'hospitalCover': random.choice([True, False]),
                    'extrasCover': random.choice([True, False]),
                    'ambulanceCover': random.choice([True, False]),
                    'overseasCover': random.choice([True, False])
                },
                'limits': {
                    'annualLimit': random.choice([1000, 2000, 3000, 5000, 10000]),
                    'dentalLimit': random.choice([500, 800, 1200, 2000]),
                    'opticalLimit': random.choice([200, 400, 600, 800])
                },
                'lastUpdated': self.fake.date_between(start_date=start_date, end_date='today').isoformat(),
                'agentId': f"AGT{self.fake.random_int(1000, 9999)}",
                'underwriter': random.choice(['nib Health', 'nib Foundation', 'nib Options'])
            }
            policies.append(policy)
        
        return policies
    
    def generate_claims(self, count: int = 10) -> List[Dict[str, Any]]:
        """Generate realistic claims data"""
        claims = []
        
        for _ in range(count):
            claim_date = self.fake.date_between(start_date='-1y', end_date='today')
            
            claim = {
                'id': self.fake.random_int(100000, 999999),
                'claimNumber': self.fake.claim_number(),
                'memberNumber': f"MBR{self.fake.random_int(100000, 999999)}",
                'policyNumber': self.fake.policy_number(),
                'claimType': self.fake.claim_type(),
                'status': self.fake.claim_status(),
                'dateOfService': claim_date.isoformat(),
                'dateSubmitted': (claim_date + timedelta(days=random.randint(1, 30))).isoformat(),
                'providerName': self.fake.company(),
                'providerNumber': self.fake.provider_number(),
                'providerType': self.fake.provider_type(),
                'serviceDescription': f"{self.fake.claim_type()} - {self.fake.catch_phrase()}",
                'totalAmount': round(random.uniform(50, 2000), 2),
                'claimedAmount': round(random.uniform(30, 1500), 2),
                'approvedAmount': round(random.uniform(25, 1200), 2),
                'excessApplied': random.choice([True, False]),
                'excessAmount': self.fake.excess_amount() if random.choice([True, False]) else 0,
                'processingTime': f"{random.randint(1, 14)} days",
                'location': {
                    'suburb': self.fake.city(),
                    'state': self.fake.australian_state(),
                    'postcode': self.fake.postcode()
                },
                'notes': self.fake.sentence(),
                'attachments': random.randint(0, 3),
                'lastUpdated': (claim_date + timedelta(days=random.randint(1, 45))).isoformat()
            }
            claims.append(claim)
        
        return claims
    
    def generate_providers(self, count: int = 10) -> List[Dict[str, Any]]:
        """Generate realistic healthcare provider data"""
        providers = []
        
        for _ in range(count):
            provider = {
                'id': self.fake.random_int(10000, 99999),
                'providerNumber': self.fake.provider_number(),
                'businessName': self.fake.company(),
                'providerType': self.fake.provider_type(),
                'speciality': random.choice([
                    'General Practice', 'Cardiology', 'Dermatology', 'Orthopedics',
                    'Psychiatry', 'Pediatrics', 'Gynecology', 'Neurology'
                ]),
                'contactPerson': {
                    'name': self.fake.name(),
                    'title': random.choice(['Dr.', 'Manager', 'Administrator', 'Director']),
                    'email': self.fake.email(),
                    'phone': self.fake.phone_number()
                },
                'address': {
                    'street': self.fake.street_address(),
                    'suburb': self.fake.city(),
                    'state': self.fake.australian_state(),
                    'postcode': self.fake.postcode()
                },
                'businessHours': {
                    'weekdays': '9:00 AM - 5:00 PM',
                    'saturday': random.choice(['9:00 AM - 1:00 PM', 'Closed']),
                    'sunday': 'Closed'
                },
                'services': random.sample([
                    'Consultations', 'Diagnostics', 'Minor Surgery', 'Vaccinations',
                    'Health Checks', 'Pathology', 'Radiology', 'Physiotherapy'
                ], k=random.randint(2, 5)),
                'accreditation': {
                    'status': random.choice(['Accredited', 'Pending', 'Expired']),
                    'expiryDate': self.fake.date_between(start_date='today', end_date='+2y').isoformat(),
                    'certifyingBody': random.choice(['ACHS', 'QIC', 'NSQHS'])
                },
                'rating': round(random.uniform(3.5, 5.0), 1),
                'totalClaims': random.randint(50, 2000),
                'averageClaimAmount': round(random.uniform(100, 800), 2),
                'status': random.choice(['Active', 'Inactive', 'Suspended']),
                'joinedDate': self.fake.date_between(start_date='-5y', end_date='-1y').isoformat(),
                'lastClaimDate': self.fake.date_between(start_date='-3m', end_date='today').isoformat()
            }
            providers.append(provider)
        
        return providers
    
    def generate_data(self, data_type: str, count: int = 10) -> List[Dict[str, Any]]:
        """Generate data based on type"""
        generators = {
            'members': self.generate_members,
            'policies': self.generate_policies, 
            'claims': self.generate_claims,
            'providers': self.generate_providers
        }
        
        if data_type not in generators:
            raise ValueError(f"Unsupported data type: {data_type}. Supported types: {list(generators.keys())}")
        
        return generators[data_type](count)