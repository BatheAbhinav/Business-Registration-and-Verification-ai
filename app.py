import streamlit as st
import json
import pandas as pd

# Title of the app
st.title('Business Registration and Verification')

# File upload functionality
uploaded_file = st.file_uploader("Choose a JSON file", type=["json"])

if uploaded_file is not None:
    # Load the data from the uploaded file
    data = json.load(uploaded_file)

    # Show summary
    summary = data['summary']
    st.subheader('Summary')
    summary_data = {
        "Total Analyzed": summary['total_analyzed'],
        "Registered Businesses": summary['registered_count'],
        "Unregistered Businesses": summary['unregistered_count'],
        "Potential Duplicates": summary['duplicate_groups_count'],
        "Area Address": summary['area_address'],
        "Search Radius (meters)": summary['search_radius_meters']
    }
    st.write(summary_data)

    # Registered Businesses section
    st.subheader('Registered Businesses')
    registered_data = []

    for business in data['registered_businesses']:
        for place in business['matched_places']:
            registered_data.append({
                "Business Name": business['input_business']['name'],
                "Category": business['input_business']['category'],
                "Timestamp": business['input_business']['timestamp'],
                "Features": ", ".join(business['input_business']['features']),
                "Matched Place Name": place['name'],
                "Normalized Name": place['normalized_name'],
                "Address": place['address'],
                "Phone": place['phone'],
                "Similarity Score": place['similarity_score'],
                "Distance (meters)": place['distance']
            })

    # Display registered businesses in a table
    if registered_data:
        registered_df = pd.DataFrame(registered_data)
        st.dataframe(registered_df)
    else:
        st.write("No registered businesses data available.")

    # Unregistered Businesses section
    st.subheader('Unregistered Businesses')
    unregistered_data = []

    for business in data['unregistered_businesses']:
        unregistered_data.append({
            "Business Name": business['name'],
            "Category": business['category'],
            "Timestamp": business['timestamp'],
            "Features": ", ".join(business['features'])
        })

    # Display unregistered businesses in a table
    if unregistered_data:
        unregistered_df = pd.DataFrame(unregistered_data)
        st.dataframe(unregistered_df)
    else:
        st.write("No unregistered businesses data available.")

    # Potential duplicates section
    st.subheader('Potential Duplicates')
    if data['potential_duplicates']:
        potential_duplicates_data = []

        for group in data['potential_duplicates']:
            for business in group:
                potential_duplicates_data.append({
                    "Business Name": business['name'],
                    "Category": business['category'],
                    "Timestamp": business['timestamp'],
                    "Features": ", ".join(business['features'])
                })

        # Display potential duplicates in a table
        potential_duplicates_df = pd.DataFrame(potential_duplicates_data)
        st.dataframe(potential_duplicates_df)
    else:
        st.write("No potential duplicates found.")
else:
    st.write("Please upload a JSON file.")

