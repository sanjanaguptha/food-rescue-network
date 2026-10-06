import streamlit as st
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if groq_api_key:
    client = Groq(api_key=groq_api_key)
else:
    client = None
from database.database import (
    create_database,
    add_donor,
    add_donation,
    add_delivery_person,
    assign_delivery_person,
    get_delivery_persons,
    update_donation_status,
    get_donation_details,
    get_admin_statistics,
    get_all_donations,
    record_distribution,
    get_category_statistics,
    get_delivered_count
)
# Page configuration
st.set_page_config(
    page_title="Food Rescue Network",
    page_icon="🍱",
    layout="wide"
)
create_database()

# Sidebar
st.sidebar.title("🍱 Food Rescue Network")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "👤 Donor Registration",
        "🎁 Donate Item",
        "🚚 Delivery Person",
        "📦 Track Donation",
        "🤝 Distribution",
        "📊 Admin Dashboard",
        "🤖 AI Assistant"
    ]
)

# Home Page
if page == "🏠 Home":

    st.title("🌱 Food Rescue Network")

    st.subheader("A Smart Donation & Distribution Management System")

    st.write("Rescue. Deliver. Make a Difference.")

    st.write(
        """
        Food Rescue Network is a platform that connects donors,
        delivery persons and people in need. Donors can register
        useful items such as food, clothes and other resources.
        Delivery persons collect these items and distribute them
        to people who need them.
        """
    )

    st.divider()

    st.subheader("🔄 How It Works")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write("👤")
        st.write("**1. Register**")
        st.caption("Donor registers with basic details.")

    with col2:
        st.write("🎁")
        st.write("**2. Donate**")
        st.caption("Register food, clothes or useful items.")

    with col3:
        st.write("🚚")
        st.write("**3. Deliver**")
        st.caption("Delivery person collects and transports items.")

    with col4:
        st.write("🤝")
        st.write("**4. Distribute**")
        st.caption("Items reach people who need them.")

    st.divider()

    st.subheader("💡 Inclusive Distribution")

    st.info(
        "Recipients do not need a smartphone or internet access. "
        "Delivery persons can identify people in need at the "
        "distribution location and provide donated items."
    )

# Donor Registration
# Donor Registration
elif page == "👤 Donor Registration":

    st.title("👤 Donor Registration")

    st.write("Please enter your details to register as a donor.")

    donor_name = st.text_input("Donor Name")

    phone = st.text_input("Phone Number")

    address = st.text_area("Address")

    email = st.text_input("Email (Optional)")

    if st.button("Register Donor"):

        if donor_name == "":
            st.error("Please enter your name.")

        elif phone == "":
            st.error("Please enter your phone number.")

        elif address == "":
            st.error("Please enter your address.")

        else:

            donor_id = add_donor(
                donor_name,
                phone,
                address,
                email
            )

            st.success("Donor registered successfully!")

            st.write("### Donor Details")

            st.write("**Donor ID:**", donor_id)
            st.write("**Name:**", donor_name)
            st.write("**Phone:**", phone)
            st.write("**Address:**", address)

            if email:
                st.write("**Email:**", email)
        


# Donate Item
elif page == "🎁 Donate Item":

    st.title("🎁 Donate an Item")

    st.write("Enter the details of the item you want to donate.")

    donor_id = st.number_input(
        "Donor ID",
        min_value=1,
        step=1
    )

    category = st.selectbox(
        "What do you want to donate?",
        ["Food", "Clothes", "Other"]
    )

    item_name = st.text_input("Item Name")

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        step=1
    )

    size = ""
    condition = ""
    description = ""

    if category == "Clothes":

        size = st.selectbox(
            "Size",
            ["S", "M", "L", "XL", "XXL", "Other"]
        )

        condition = st.selectbox(
            "Condition",
            ["New", "Good", "Used"]
        )

        description = st.text_area(
            "Description"
        )

    elif category == "Food":

        description = st.text_area(
            "Food Description"
        )

    else:

        condition = st.selectbox(
            "Condition",
            ["New", "Good", "Used"]
        )

        description = st.text_area(
            "Description"
        )

    if st.button("Register Donation"):

        if item_name == "":
            st.error("Please enter the item name.")

        else:

            donation_id = add_donation(
                donor_id,
                category,
                item_name,
                quantity,
                size,
                description,
                condition
            )

            st.success(
                "Donation registered successfully!"
            )

            st.write(
                "**Donation ID:**",
                donation_id
            )

            st.write(
                "**Category:**",
                category
            )

            st.write(
                "**Item:**",
                item_name
            )

            st.write(
                "**Quantity:**",
                quantity
            )

            st.write(
                "**Status:** REGISTERED"
            )



# Delivery Person
elif page == "🚚 Delivery Person":

    st.title("🚚 Delivery Person")

    st.write(
        "Register a delivery person who can collect "
        "donations from donors and distribute them."
    )

    delivery_name = st.text_input("Delivery Person Name")

    delivery_phone = st.text_input("Contact Number")

    delivery_address = st.text_area(
        "Address"
    )

    if st.button("Register Delivery Person"):

        if delivery_name == "":
            st.error("Please enter the delivery person's name.")

        elif delivery_phone == "":
            st.error("Please enter the contact number.")

        else:

            delivery_id = add_delivery_person(
                delivery_name,
                delivery_phone,
                delivery_address
            )

            st.success(
                "Delivery person registered successfully!"
            )

            st.write("### Delivery Person Details")

            st.write(
                "**Delivery ID:**",
                delivery_id
            )

            st.write(
                "**Name:**",
                delivery_name
            )

            st.write(
                "**Phone:**",
                delivery_phone
            )

            st.write(
                "**Address:**",
                delivery_address
            )

    # Update Donation Status
    st.divider()

    st.subheader("📦 Update Donation Status")

    status_donation_id = st.number_input(
        "Donation ID for Status Update",
        min_value=1,
        step=1
    )

    new_status = st.selectbox(
        "Select New Status",
        [
            "PICKED UP",
            "OUT FOR DELIVERY",
            "DELIVERED"
        ]
    )

    if st.button("Update Donation Status"):

        update_donation_status(
            status_donation_id,
            new_status
        )

        st.success(
            f"Donation {status_donation_id} status updated to {new_status}."
        )


# Track Donation
# Track Donation
elif page == "📦 Track Donation":

    st.title("📦 Donation Management")

    # ==========================================
    # ASSIGN DELIVERY PERSON
    # ==========================================

    st.subheader("🚚 Assign Delivery Person")

    st.write(
        "Assign a registered delivery person to a donation."
    )

    donation_id_assign = st.number_input(
        "Donation ID",
        min_value=1,
        step=1,
        key="assign_donation_id"
    )

    delivery_persons = get_delivery_persons()

    if delivery_persons:

        delivery_options = {}

        for person in delivery_persons:

            delivery_id = person[0]
            name = person[1]
            phone = person[2]

            delivery_options[
                f"{name} - {phone}"
            ] = delivery_id

        selected_person = st.selectbox(
            "Select Delivery Person",
            list(delivery_options.keys())
        )

        if st.button("Assign Delivery Person"):

            selected_delivery_id = delivery_options[
                selected_person
            ]

            assign_delivery_person(
                donation_id_assign,
                selected_delivery_id
            )

            st.success(
                "Delivery person assigned successfully!"
            )

            st.write(
                "**Donation ID:**",
                donation_id_assign
            )

            st.write(
                "**Delivery Person:**",
                selected_person
            )

            st.write(
                "**Status:** ASSIGNED"
            )

    else:

        st.warning(
            "No delivery persons are registered yet."
        )

    st.divider()

    # ==========================================
    # TRACK DONATION
    # ==========================================

    # ==============================
# TRACK DONATION
# ==============================

elif page == "📦 Track Donation":

    st.title("📦 Track Donation")

    st.write(
        "Enter your Donation ID to view the complete donation journey."
    )

    donation_id = st.number_input(
        "Donation ID",
        min_value=1,
        step=1
    )

    if st.button("🔍 Track Donation"):

        donation = get_donation_details(donation_id)

        if donation:

            # ==============================
            # DONATION INFORMATION
            # ==============================

            st.success("✅ Donation found!")

            st.subheader("📋 Donation Details")

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    "**Donation ID:**",
                    donation[0]
                )

                st.write(
                    "**Category:**",
                    donation[1]
                )

                st.write(
                    "**Item:**",
                    donation[2]
                )

            with col2:

                st.write(
                    "**Quantity:**",
                    donation[3]
                )

                if donation[4]:

                    st.write(
                        "**Size:**",
                        donation[4]
                    )

                if donation[6]:

                    st.write(
                        "**Condition:**",
                        donation[6]
                    )

            if donation[5]:

                st.write(
                    "**Description:**",
                    donation[5]
                )

            st.divider()

            # ==============================
            # DONOR DETAILS
            # ==============================

            st.subheader("👤 Donor Details")

            st.write(
                "**Name:**",
                donation[8]
            )

            st.write(
                "**Phone:**",
                donation[9]
            )

            st.write(
                "**Address:**",
                donation[10]
            )

            st.divider()

            # ==============================
            # DELIVERY DETAILS
            # ==============================

            st.subheader("🚚 Delivery Details")

            if donation[11]:

                st.write(
                    "**Delivery Person:**",
                    donation[11]
                )

                st.write(
                    "**Phone:**",
                    donation[12]
                )

            else:

                st.info(
                    "🚚 A delivery person has not been assigned yet."
                )

            st.divider()

            # ==============================
            # DELIVERY STATUS
            # ==============================

            st.subheader("📍 Current Status")

            status = donation[7]

            st.success(
                f"Current Status: {status}"
            )

            # ==============================
            # PROGRESS
            # ==============================

            st.subheader("🛣️ Donation Journey")

            statuses = [
                "REGISTERED",
                "ASSIGNED",
                "PICKED UP",
                "OUT FOR DELIVERY",
                "DELIVERED"
            ]

            current_index = statuses.index(status)

            for i, step in enumerate(statuses):

                if i <= current_index:

                    st.success(
                        f"✅ {step}"
                    )

                else:

                    st.info(
                        f"⬜ {step}"
                    )

                if i < len(statuses) - 1:

                    st.write("↓")

        else:

            st.error(
                "❌ Donation not found. Please check the Donation ID."
            )
# ==============================
# DISTRIBUTION
# ==============================

elif page == "🤝 Distribution":

    st.title("🤝 Distribution")

    st.write(
        "Record the person and location where a donation was distributed."
    )

    donation_id = st.number_input(
        "Donation ID",
        min_value=1,
        step=1
    )

    recipient_name = st.text_input(
        "Recipient Name"
    )

    location = st.text_input(
        "Distribution Location"
    )

    st.info(
        "Recipient phone number is not required. "
        "This supports people who may not have a phone."
    )

    if st.button("Record Distribution"):

        if recipient_name.strip() == "":
            st.error("Please enter the recipient name.")

        elif location.strip() == "":
            st.error("Please enter the distribution location.")

        else:
            record_distribution(
            donation_id,
            recipient_name,
            location
            )

            update_donation_status(
                donation_id,
                "DELIVERED"
            )

            st.success(
                "Donation successfully distributed!"
            )

            st.write("**Donation ID:**", donation_id)
            st.write("**Recipient:**", recipient_name)
            st.write("**Location:**", location)
            st.write("**Status:** DELIVERED")
            
# Admin Dashboard
# Admin Dashboard
# ==============================
# ADMIN DASHBOARD
# ==============================

elif page == "📊 Admin Dashboard":

    st.title("📊 Admin Dashboard")

    st.write(
        "Overview of the Food Rescue Network."
    )

    # Get statistics
    (
        total_donors,
        total_donations,
        total_delivery_persons,
        status_counts
    ) = get_admin_statistics()

    delivered_count = get_delivered_count()

    category_counts = get_category_statistics()

    # ==============================
    # SUMMARY CARDS
    # ==============================

    st.subheader("📌 Overall Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "👤 Total Donors",
            total_donors
        )

    with col2:

        st.metric(
            "🎁 Total Donations",
            total_donations
        )

    with col3:

        st.metric(
            "🚚 Delivery Persons",
            total_delivery_persons
        )

    with col4:

        st.metric(
            "✅ Delivered",
            delivered_count
        )

    st.divider()

    # ==============================
    # DONATION CATEGORIES
    # ==============================

    st.subheader("🎁 Donation Categories")

    if category_counts:

        category_data = pd.DataFrame(
            category_counts,
            columns=["Category", "Count"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.dataframe(
                category_data,
                use_container_width=True,
                hide_index=True
            )

        with col2:

            st.bar_chart(
                category_data.set_index("Category")
            )

    else:

        st.info(
            "No donation category data available."
        )

    st.divider()

    # ==============================
    # DONATION STATUS
    # ==============================

    st.subheader("📦 Donation Status")

    if status_counts:

        status_data = pd.DataFrame(
            status_counts,
            columns=["Status", "Count"]
        )

        st.bar_chart(
            status_data.set_index("Status")
        )

    else:

        st.info(
            "No donation status data available."
        )

    st.divider()

    # ==============================
    # ALL DONATIONS
    # ==============================

    st.subheader("📋 All Donations")

    donations = get_all_donations()

    if donations:

        donation_data = pd.DataFrame(
            donations,
            columns=[
                "Donation ID",
                "Category",
                "Item",
                "Quantity",
                "Status",
                "Created At"
            ]
        )

        st.dataframe(
            donation_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No donations available."
        )
# AI Assistant

# ==============================
# SMART CHATBOT
# ==============================

elif page == "🤖 AI Assistant":

    st.title("🤖 Smart Donation Assistant")

    st.write(
        "Welcome! I can help you understand the Food Rescue Network."
    )

    # Clear chat button
    if st.button("🧹 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    # Create chat history
    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 I am your Donation Assistant. "
                    "You can ask me about donations, delivery, "
                    "tracking or distribution."
                )
            }
        ]

    # Display chat history
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    # Suggested questions
    st.subheader("💡 Suggested Questions")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🍱 What can I donate?"):

            user_question = "What can I donate?"

        elif st.button("🚚 How does delivery work?"):

            user_question = "How does delivery work?"

    with col2:

        if st.button("📦 How can I track a donation?"):

            user_question = "How can I track a donation?"

        elif st.button("🤝 What is distribution?"):

            user_question = "What is distribution?"

    # Chat input
    typed_question = st.chat_input(
        "Ask your question..."
    )

    if typed_question:

        user_question = typed_question

    # Process question
    if "user_question" in locals():

        # Show user message
        with st.chat_message("user"):

            st.write(user_question)

        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })

        question = user_question.lower()

        # ==============================
        # RESPONSES
        # ==============================

        if "what can i donate" in question:

            answer = (
                "You can donate suitable food, clean clothes, "
                "and other useful items that are in good condition."
            )

        elif "food" in question and "donate" in question:

            answer = (
                "You can donate suitable and safe food items. "
                "Enter the food name, quantity and description "
                "when registering the donation."
            )

        elif "clothes" in question:

            answer = (
                "You can donate clean and usable clothes. "
                "For clothes, enter the size, quantity, condition "
                "and description."
            )

        elif "delivery" in question:

            answer = (
                "A delivery person collects the donation from "
                "the donor and takes it to the distribution location."
            )

        elif "track" in question or "status" in question:

            answer = (
                "Open the Track Donation page, enter your Donation ID "
                "and click Track Donation to see the current status."
            )

        elif "distribution" in question:

            answer = (
                "Distribution is the final stage where the donated "
                "item is given to a person in need."
            )

        elif "how does" in question or "how it works" in question:

            answer = (
                "The process is: Donor Registration → Donation → "
                "Delivery Person → Pickup → Distribution → Delivered."
            )

        elif "without phone" in question or "no phone" in question:

            answer = (
                "Yes. A recipient does not need a smartphone. "
                "The delivery person can identify people in need "
                "at the distribution location."
            )

        elif "hello" in question or "hi" in question:

            answer = (
                "Hello! 👋 How can I help you with the Food Rescue Network?"
            )

        else:

            answer = (
                "I can help with food donations, clothes donations, "
                "delivery, tracking and distribution. "
                "Try asking one of these topics."
            )

        # Show assistant response
        with st.chat_message("assistant"):

            st.write(answer)

        # Save response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })