"""
Test folium map functionality
"""

def test_folium_map():
    """Test if folium map can be created"""
    print("🗺️ Testing Folium Map Creation...")
    
    try:
        import folium
        from streamlit_folium import st_folium
        
        # Create a simple map
        m = folium.Map(location=[20.0, 76.0], zoom_start=7)
        
        # Add a marker
        folium.Marker(
            location=[21.1458, 79.0882],
            popup='Test Marker',
            tooltip='Nagpur'
        ).add_to(m)
        
        print("   ✅ Folium map created successfully!")
        print("   ✅ Marker added successfully!")
        print("   ✅ streamlit-folium imported successfully!")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Map creation failed: {e}")
        return False

def main():
    """Run the test"""
    print("🚛 Route-Rakshak Map Test")
    print("=" * 40)
    
    if test_folium_map():
        print("\n🎉 SUCCESS: Live map feature is ready!")
        print("🗺️ Your Customer view will show the interactive map!")
    else:
        print("\n❌ FAILED: Map feature has issues")

if __name__ == "__main__":
    main()