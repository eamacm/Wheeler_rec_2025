import pandas as pd
import argparse
import re

def reheader_csv(csv):
    # Define the new header list
    new_headers = [
        "timestamp", "email_address", "adult1_last_name", "adult1_first_name", "adult2_last_name", "adult2_first_name",
        "street_address", "town", "zip_code", "email1", "email2", "phone1", "phone2", "rules_agreed", "membership_type",
        "swimming_member_count", "has_under18_members", "rules_reviewed_with_children",
        "child1_first_name", "child1_last_name", "child1_dob", "age_1", "allergies_1", "child1_swim_interest",
        "child1_last_lesson", "child1_2025_level", "more_children_1",
        "child2_first_name", "child2_last_name", "child2_dob", "age_2", "allergies_2", "child2_swim_interest",
        "child2_last_lesson", "child2_2025_level", "more_children_2",
        "child3_first_name", "child3_last_name", "child3_dob", "age_3", "allergies_3", "child3_swim_interest",
        "child3_last_lesson", "child3_2025_level", "more_children_3",
        "child4_first_name", "child4_last_name", "child4_dob", "age_4", "allergies_4", "child4_swim_interest",
        "child4_last_lesson", "child4_2025_level", "more_children_4",
        "child5_first_name", "child5_last_name", "child5_dob", "age_5", "allergies_5", "child5_swim_interest",
        "child5_last_lesson", "child5_2025_level", "more_children_5",
        "child6_first_name", "child6_last_name", "child6_dob", "age_6", "allergies_6", "child6_swim_interest",
        "child6_last_lesson", "child6_2025_level", "more_children_6",
        "child7_first_name", "child7_last_name", "child7_dob", "age_7", "allergies_7", "child7_swim_interest",
        "child7_last_lesson", "child7_2025_level",
        "weekend_lessons_counts", "weekend_addn_comments", "caregiver_present", "caregiver_name",
        "caregiver_address", "caregiver_phone", "caregiver_days", "allow_pool_alone_9plus",
        "guardian1_name", "guardian1_phone", "guardian2_name", "guardian2_phone",
        "local_contact1_name", "local_contact1_phone", "local_contact2_name", "local_contact2_phone",
        "emergency_leave_permission", "solo_permission", "rules_reviewed_full", "orientation_attended",
        "volunteer_committees", "work_detail_commitment", "work_duty_selected"
    ]
    # Load the CSV, skipping the original header row
    df = pd.read_csv(csv, header=0)  # header=0 will load the first row as data
    
    # Assign new headers
    df.columns = new_headers
    new_csv=df#new_csv=df.to_csv("reheader.csv", index=False)
    return new_csv

def parse_work_duty_date(duty_string):
    """Extracts the first MM/DD date from the work duty string."""
    if pd.isna(duty_string):
        return ""
    match = re.search(r"\((\d{1,2}/\d{1,2})", duty_string)
    if match:
        return match.group(1)
    return ""

def create_work_duty_df(df):
    work_duty_rows = []

    for idx, row in df.iterrows():
        duty = str(row.get("work_duty_selected", "")).strip()
        
        # Skip if no duty was selected
        if not duty or pd.isna(row.get("work_duty_selected")):
            continue

        last_name1 = str(row.get("adult1_last_name", "")).strip()
        last_name2 = str(row.get("adult2_last_name", "")).strip()

        if last_name1 and pd.notna(row.get("adult2_last_name")) and last_name2 and last_name1 != last_name2:
            family_name = f"{last_name1}-{last_name2}"
        else:
            family_name = last_name1 or last_name2

        duty_date = parse_work_duty_date(duty)

        work_row = {
            "Family Name": family_name,
            "Email 1": row.get("email1", ""),
            "Email 2": row.get("email2", ""),
            "Work Duty": duty,
            "Work Duty Date": duty_date
        }

        work_duty_rows.append(work_row)

    return pd.DataFrame(work_duty_rows)
    
def make_emergency_contact_child_df(df):
    child_rows = []

    for idx, row in df.iterrows():
        for i in range(1, 8):  # children 1 to 7
            first_name = row.get(f"child{i}_first_name", "")
            last_name = row.get(f"child{i}_last_name", "")
            age = row.get(f"age_{i}", "")

            if pd.notna(first_name) or pd.notna(last_name):  # skip empty child slots
                child_row = {
                    "CHILD LAST NAME": last_name,
                    "CHILD FIRST NAME": first_name,
                    "Age as of 6/1/2023": age,
                    "MEMBER ADULT #1": str(row.get("adult1_first_name", "")) + " " + str(row.get("adult1_last_name", "")),
                    "Phone Number Member Adult #1": row.get("phone1", ""),
                    "MEMBER ADULT #2": str(row.get("adult2_first_name", "")) + " " + str(row.get("adult2_last_name", "")),
                    "Phone Number Member Adult #2": row.get("phone2", ""),
                    "Emergency Contact #1": row.get("local_contact1_name", ""),
                    "Emergency Contact Number #1": row.get("local_contact1_phone", ""),
                    "Emergency Contact #2": row.get("local_contact2_name", ""),
                    "Emergency Contact Number #2": row.get("local_contact2_phone", ""),
                    "9+ Pool Alone Allowed": row.get("allow_pool_alone_9plus", ""),
                    "Rules Reviewed With Children": row.get("rules_reviewed_with_children", ""),
                    "Orientation Attended": row.get("orientation_attended", ""),
                    "Emergency Leave Permission": row.get("emergency_leave_permission", ""),
                    "Regular Caregiver?": row.get("caregiver_present", ""),
                }
                child_rows.append(child_row)

    child_df = pd.DataFrame(child_rows)
    return child_df

def main():
    parser = argparse.ArgumentParser(description="Reheader a CSV file with a predefined set of column names.")
    parser.add_argument("input_csv", help="Path to the input CSV file")
    args = parser.parse_args()
    
    new_csv = reheader_csv(args.input_csv)
    emergency_csv=make_emergency_contact_child_df(new_csv)
    emergency_csv.to_csv("emergency_contacts.csv", index=False)
    work_duty_prep = create_work_duty_df(new_csv)
    work_duty_prep.to_csv("work_duties_full.csv", index=False)
    

if __name__ == "__main__":
    main()