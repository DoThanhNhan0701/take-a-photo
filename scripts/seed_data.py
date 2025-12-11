"""
Seed data script for locations and categories tables
Run this script to populate initial data
"""
import sys
import os

# Add the parent directory to the path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.location import Location
from app.models.category import Category
import uuid


def seed_locations(db: Session):
    """Seed 30 sample locations (supermarkets/stores in Da Nang and nearby)"""
    
    locations_data = [
        # Da Nang City
        {"name": "CoopMart Hải Châu", "code": "CM_HC", "address": "515 Hùng Vương, Hải Châu, Đà Nẵng", "gps_latitude": 16.0544, "gps_longitude": 108.2022},
        {"name": "Big C Đà Nẵng", "code": "BC_DN", "address": "255-257 Hùng Vương, Hải Châu, Đà Nẵng", "gps_latitude": 16.0544, "gps_longitude": 108.2011},
        {"name": "Lotte Mart Đà Nẵng", "code": "LT_DN", "address": "Nguyễn Hữu Thọ, Hải Châu, Đà Nẵng", "gps_latitude": 16.0471, "gps_longitude": 108.2242},
        {"name": "Vinmart Lê Duẩn", "code": "VM_LD", "address": "48 Lê Duẩn, Hải Châu, Đà Nẵng", "gps_latitude": 16.0678, "gps_longitude": 108.2211},
        {"name": "Vinmart+ Nguyễn Hữu Thọ", "code": "VMP_NHT", "address": "120 Nguyễn Hữu Thọ, Hải Châu, Đà Nẵng", "gps_latitude": 16.0522, "gps_longitude": 108.2244},
        {"name": "CoopMart Cẩm Lệ", "code": "CM_CL", "address": "Cẩm Lệ, Đà Nẵng", "gps_latitude": 16.0289, "gps_longitude": 108.1789},
        {"name": "Mega Market Đà Nẵng", "code": "MM_DN", "address": "Hoàng Văn Thái, Thanh Khê, Đà Nẵng", "gps_latitude": 16.0544, "gps_longitude": 108.1678},
        {"name": "Vinmart Thanh Khê", "code": "VM_TK", "address": "200 Lê Duẩn, Thanh Khê, Đà Nẵng", "gps_latitude": 16.0689, "gps_longitude": 108.1911},
        {"name": "Siêu thị Vạn Hạnh", "code": "VH_DN", "address": "Hải Châu, Đà Nẵng", "gps_latitude": 16.0644, "gps_longitude": 108.2122},
        {"name": "CoopFood Hải Châu", "code": "CF_HC", "address": "Lê Duẩn, Hải Châu, Đà Nẵng", "gps_latitude": 16.0656, "gps_longitude": 108.2156},
        
        # More Danang locations
        {"name": "Vinmart Ngũ Hành Sơn", "code": "VM_NHS", "address": "Ngũ Hành Sơn, Đà Nẵng", "gps_latitude": 16.0022, "gps_longitude": 108.2511},
        {"name": "Circle K Trần Phú", "code": "CK_TP", "address": "125 Trần Phú, Hải Châu, Đà Nẵng", "gps_latitude": 16.0544, "gps_longitude": 108.2289},
        {"name": "Ministop Lê Lợi", "code": "MS_LL", "address": "55 Lê Lợi, Hải Châu, Đà Nẵng", "gps_latitude": 16.0689, "gps_longitude": 108.2244},
        {"name": "FamilyMart Bạch Đằng", "code": "FM_BD", "address": "200 Bạch Đằng, Hải Châu, Đà Nẵng", "gps_latitude": 16.0711, "gps_longitude": 108.2278},
        {"name": "GS25 Điện Biên Phủ", "code": "GS_DBP", "address": "350 Điện Biên Phủ, Thanh Khê, Đà Nẵng", "gps_latitude": 16.0556, "gps_longitude": 108.1922},
        {"name": "Vinmart Sơn Trà", "code": "VM_ST", "address": "Sơn Trà, Đà Nẵng", "gps_latitude": 16.0844, "gps_longitude": 108.2444},
        {"name": "CoopMart Liên Chiểu", "code": "CM_LC", "address": "Liên Chiểu, Đà Nẵng", "gps_latitude": 16.0711, "gps_longitude": 108.1456},
        {"name": "Siêu thị Hòa Phát", "code": "HP_DN", "address": "Thanh Khê, Đà Nẵng", "gps_latitude": 16.0578, "gps_longitude": 108.1789},
        {"name": "Vinmart Hoàng Sa", "code": "VM_HS", "address": "100 Hoàng Sa, Thanh Khê, Đà Nẵng", "gps_latitude": 16.0622, "gps_longitude": 108.1856},
        {"name": "Circle K Nguyễn Tất Thành", "code": "CK_NTT", "address": "Nguyễn Tất Thành, Liên Chiểu, Đà Nẵng", "gps_latitude": 16.0722, "gps_longitude": 108.1533},
        
        # Hội An
        {"name": "CoopMart Hội An", "code": "CM_HA", "address": "Hội An, Quảng Nam", "gps_latitude": 15.8801, "gps_longitude": 108.3380},
        {"name": "Vinmart Hội An", "code": "VM_HA", "address": "Trần Phú, Hội An, Quảng Nam", "gps_latitude": 15.8789, "gps_longitude": 108.3267},
        
        # Tam Kỳ
        {"name": "Big C Tam Kỳ", "code": "BC_TK", "address": "Tam Kỳ, Quảng Nam", "gps_latitude": 15.5736, "gps_longitude": 108.4739},
        {"name": "Vinmart Tam Kỳ", "code": "VM_TKY", "address": "Tam Kỳ, Quảng Nam", "gps_latitude": 15.5689, "gps_longitude": 108.4656},
        
        # Huế
        {"name": "BigC Huế", "code": "BC_HUE", "address": "51 Hùng Vương, Huế", "gps_latitude": 16.4637, "gps_longitude": 107.5909},
        {"name": "CoopMart Huế", "code": "CM_HUE", "address": "Lê Duẩn, Huế", "gps_latitude": 16.4544, "gps_longitude": 107.5889},
        {"name": "Vinmart Huế", "code": "VM_HUE", "address": "Trần Hưng Đạo, Huế", "gps_latitude": 16.4589, "gps_longitude": 107.5967},
        
        # Quảng Ngãi
        {"name": "CoopMart Quảng Ngãi", "code": "CM_QN", "address": "Quảng Ngãi", "gps_latitude": 15.1214, "gps_longitude": 108.8044},
        {"name": "Vinmart Quảng Ngãi", "code": "VM_QN", "address": "Quảng Ngãi", "gps_latitude": 15.1189, "gps_longitude": 108.7989},
        
        # Kon Tum
        {"name": "Siêu thị Kon Tum", "code": "ST_KT", "address": "Kon Tum", "gps_latitude": 14.3545, "gps_longitude": 108.0004},
    ]
    
    print("Seeding locations...")
    count = 0
    for loc_data in locations_data:
        # Check if location already exists
        existing = db.query(Location).filter(Location.code == loc_data["code"]).first()
        if not existing:
            location = Location(**loc_data)
            db.add(location)
            count += 1
    
    db.commit()
    print(f"✓ Added {count} locations")


def seed_categories(db: Session):
    """Seed 30 sample categories (invoice types)"""
    
    categories_data = [
        # Grocery & Food
        {"name": "Thực phẩm tươi sống", "code": "TPTS", "icon_name": "ic_food_fresh", "description": "Rau, củ, quả, thịt, cá tươi sống", "is_active": True},
        {"name": "Thực phẩm đông lạnh", "code": "TPDL", "icon_name": "ic_frozen", "description": "Thực phẩm đông lạnh, kem", "is_active": True},
        {"name": "Thực phẩm khô", "code": "TPK", "icon_name": "ic_dry_food", "description": "Gạo, bột, đường, muối", "is_active": True},
        {"name": "Đồ uống", "code": "DU", "icon_name": "ic_drink", "description": "Nước ngọt, bia, rượu, nước ép", "is_active": True},
        {"name": "Sữa - Bơ - Phô mai", "code": "SBP", "icon_name": "ic_dairy", "description": "Sản phẩm từ sữa", "is_active": True},
        {"name": "Bánh kẹo", "code": "BK", "icon_name": "ic_candy", "description": "Bánh ngọt, kẹo, snack", "is_active": True},
        
        # Personal Care
        {"name": "Hóa mỹ phẩm", "code": "HMP", "icon_name": "ic_cosmetics", "description": "Mỹ phẩm, son phấn, nước hoa", "is_active": True},
        {"name": "Chăm sóc cá nhân", "code": "CSCP", "icon_name": "ic_personal_care", "description": "Dầu gội, sữa tắm, kem đánh răng", "is_active": True},
        {"name": "Vệ sinh nhà cửa", "code": "VSNC", "icon_name": "ic_cleaning", "description": "Nước giặt, nước rửa chén", "is_active": True},
        
        # Health
        {"name": "Thực phẩm chức năng", "code": "TPCN", "icon_name": "ic_supplement", "description": "Vitamin, thực phẩm bổ sung", "is_active": True},
        {"name": "Dược phẩm", "code": "DP", "icon_name": "ic_medicine", "description": "Thuốc không kê đơn", "is_active": True},
        {"name": "Thiết bị y tế", "code": "TBYT", "icon_name": "ic_medical", "description": "Khẩu trang, nhiệt kế", "is_active": True},
        
        # Home & Living
        {"name": "Đồ gia dụng", "code": "DGD", "icon_name": "ic_home", "description": "Chén, dĩa, dao, kéo", "is_active": True},
        {"name": "Điện gia dụng", "code": "DGGD", "icon_name": "ic_appliance", "description": "Quạt, bàn ủi, bình đun", "is_active": True},
        {"name": "Nội thất", "code": "NT", "icon_name": "ic_furniture", "description": "Bàn, ghế, tủ", "is_active": True},
        {"name": "Đồ trang trí", "code": "DTT", "icon_name": "ic_decoration", "description": "Tranh, lọ hoa, đèn", "is_active": True},
        
        # Fashion
        {"name": "Thời trang nam", "code": "TTN", "icon_name": "ic_man", "description": "Quần áo nam", "is_active": True},
        {"name": "Thời trang nữ", "code": "TTNU", "icon_name": "ic_woman", "description": "Quần áo nữ", "is_active": True},
        {"name": "Thời trang trẻ em", "code": "TTTE", "icon_name": "ic_kids", "description": "Quần áo trẻ em", "is_active": True},
        {"name": "Giày dép", "code": "GD", "icon_name": "ic_shoes", "description": "Giày, dép các loại", "is_active": True},
        {"name": "Phụ kiện thời trang", "code": "PKTT", "icon_name": "ic_accessories", "description": "Túi xách, mũ, kính", "is_active": True},
        
        # Electronics
        {"name": "Điện thoại - Máy tính bảng", "code": "DTMT", "icon_name": "ic_phone", "description": "Smartphone, tablet", "is_active": True},
        {"name": "Laptop - Máy tính", "code": "LTMT", "icon_name": "ic_laptop", "description": "Laptop, PC, linh kiện", "is_active": True},
        {"name": "Thiết bị âm thanh", "code": "TBAT", "icon_name": "ic_audio", "description": "Tai nghe, loa", "is_active": True},
        
        # Baby & Kids
        {"name": "Mẹ và bé", "code": "MVB", "icon_name": "ic_baby", "description": "Sữa bột, tã, đồ dùng cho bé", "is_active": True},
        {"name": "Đồ chơi", "code": "DC", "icon_name": "ic_toy", "description": "Đồ chơi trẻ em", "is_active": True},
        
        # Books & Stationery
        {"name": "Sách - Văn phòng phẩm", "code": "SVP", "icon_name": "ic_book", "description": "Sách, vở, bút", "is_active": True},
        
        # Sports
        {"name": "Thể thao", "code": "TT", "icon_name": "ic_sports", "description": "Dụng cụ thể thao", "is_active": True},
        
        # Pets
        {"name": "Thú cưng", "code": "TC", "icon_name": "ic_pet", "description": "Thức ăn, đồ dùng cho thú cưng", "is_active": True},
        
        # Other
        {"name": "Khác", "code": "OTHER", "icon_name": "ic_other", "description": "Các mặt hàng khác", "is_active": True},
    ]
    
    print("Seeding categories...")
    count = 0
    for cat_data in categories_data:
        # Check if category already exists
        existing = db.query(Category).filter(Category.code == cat_data["code"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)
            count += 1
    
    db.commit()
    print(f"✓ Added {count} categories")


def main():
    """Main function to seed data"""
    print("Starting data seeding...")
    print("=" * 50)
    
    db = SessionLocal()
    try:
        seed_locations(db)
        seed_categories(db)
        print("=" * 50)
        print("✓ Data seeding completed successfully!")
    except Exception as e:
        print(f"✗ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
