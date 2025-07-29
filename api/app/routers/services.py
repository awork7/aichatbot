from fastapi import APIRouter
from app.models.response import ServicesResponse, ServiceInfo
from typing import List

router = APIRouter()

@router.get("/", response_model=ServicesResponse)
async def get_banking_services():
    """Get all available banking services"""
    services = [
        ServiceInfo(
            id=1,
            name="Savings Accounts",
            description="Various savings account options with competitive interest rates",
            icon="💰",
            category="accounts"
        ),
        ServiceInfo(
            id=2,
            name="Home Loans",
            description="Home loan solutions with flexible terms",
            icon="🏠",
            category="loans"
        ),
        ServiceInfo(
            id=3,
            name="Personal Loans",
            description="Quick personal loans for your needs",
            icon="💳",
            category="loans"
        ),
        ServiceInfo(
            id=4,
            name="Credit Cards",
            description="Premium credit cards with rewards",
            icon="💸",
            category="cards"
        ),
        ServiceInfo(
            id=5,
            name="Fixed Deposits",
            description="Secure investment options with guaranteed returns",
            icon="📈",
            category="investments"
        ),
        ServiceInfo(
            id=6,
            name="Current Accounts",
            description="Business and individual current accounts",
            icon="🏢",
            category="accounts"
        ),
        ServiceInfo(
            id=7,
            name="Digital Banking",
            description="Online and mobile banking services",
            icon="📱",
            category="digital"
        ),
        ServiceInfo(
            id=8,
            name="Customer Support",
            description="24/7 customer service and support",
            icon="📞",
            category="support"
        )
    ]
    
    return ServicesResponse(services=services, total=len(services))

@router.get("/categories")
async def get_service_categories():
    """Get service categories"""
    return {
        "categories": [
            {"id": "accounts", "name": "Accounts", "icon": "🏦"},
            {"id": "loans", "name": "Loans", "icon": "💰"},
            {"id": "cards", "name": "Cards", "icon": "💳"},
            {"id": "investments", "name": "Investments", "icon": "📈"},
            {"id": "digital", "name": "Digital Services", "icon": "📱"},
            {"id": "support", "name": "Support", "icon": "🎧"}
        ]
    }
