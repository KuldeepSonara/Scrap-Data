import json
import html
import re


course_type_mapping = {
    1: "Bachelor's degree",
    2: "Master's degree",
    3: "PhD / Doctorate",
    4: "Cross-faculty graduate and research school",
    5: "Prep course",
    6: "Language course",
    7: "Short course"
}


subject_mapping = {
    "Engineering": [
        {"id": 11, "name": "Engineering in general"},
        {"id": 12, "name": "Architecture"},
        {"id": 13, "name": "Civil Engineering"},
        {"id": 14, "name": "Electrical Engineering"},
        {"id": 15, "name": "Mechanical Engineering / Process Engineering"},
        {"id": 16, "name": "Mining, Metallurgy"},
        {"id": 17, "name": "Surveying"},
        {"id": 18, "name": "Town and Country Planning"},
        {"id": 19, "name": "Transport Engineering, Nautical Science"}
    ],
    "Languages and Cultural Studies": [
        {"id": 20, "name": "Languages and Cultural Studies in general"},
        {"id": 21, "name": "Catholic Theology"},
        {"id": 22, "name": "Civilisation Studies in the narrower sense"},
        {"id": 23, "name": "Classical Philology"},
        {"id": 24, "name": "Education"},
        {"id": 25, "name": "English Studies, American Studies"},
        {"id": 26, "name": "General and Comparative Literature and Linguistics"},
        {"id": 27, "name": "German Language and Literature (German, Germanic Languages except English)"},
        {"id": 28, "name": "History"},
        {"id": 29, "name": "Library, Documentation and Media Studies"},
        {"id": 30, "name": "Other / Non-European Languages and Cultural Studies"},
        {"id": 31, "name": "Philosophy"},
        {"id": 32, "name": "Protestant Theology"},
        {"id": 33, "name": "Psychology"},
        {"id": 34, "name": "Romance Languages"},
        {"id": 35, "name": "Slavonic, Baltic, Finno-Ugrian Studies"},
        {"id": 36, "name": "Special Education"}
    ],
    "Law, Economics and Social Sciences": [
        {"id": 37, "name": "Law, Economics and Social Sciences in general"},
        {"id": 38, "name": "Business and Economics"},
        {"id": 39, "name": "Industrial Engineering"},
        {"id": 40, "name": "Law"},
        {"id": 41, "name": "Political Science"},
        {"id": 42, "name": "Public Administration"},
        {"id": 43, "name": "Regional Studies"},
        {"id": 44, "name": "Social Science"},
        {"id": 45, "name": "Social Services"}
    ],
    "Mathematics, Natural Sciences": [
        {"id": 46, "name": "Mathematics, Natural Sciences in general"},
        {"id": 47, "name": "Biology"},
        {"id": 48, "name": "Chemistry"},
        {"id": 49, "name": "Computer Science"},
        {"id": 50, "name": "Earth Sciences (excluding Geography)"},
        {"id": 51, "name": "Geography"},
        {"id": 52, "name": "Mathematics"},
        {"id": 53, "name": "Pharmacy"},
        {"id": 54, "name": "Physics, Astronomy"}
    ],
    "Medicine": [
        {"id": 55, "name": "Medicine in general"},
        {"id": 56, "name": "Clinical, Practical Medicine (excluding Dentistry)"},
        {"id": 57, "name": "Clinical, Theoretical Medicine (including Dentistry)"},
        {"id": 58, "name": "Dentistry (Clinical, Practical)"},
        {"id": 59, "name": "Pre-clinical Medical Studies (including Dentistry)"}
    ],
    "Sport": [
        {"id": 60, "name": "Sport"}
    ],
    "Veterinary Medicine": [
        {"id": 61, "name": "Veterinary Medicine in general"},
        {"id": 62, "name": "Clinical Practical Veterinary Medicine"},
        {"id": 63, "name": "Clinical Theoretical Veterinary Medicine"},
        {"id": 64, "name": "Pre-clinical Veterinary Medicine"}
    ],
    "German Language": [
        {"id": 65, "name": "German Language Course (including Literature and Culture Studies)"},
        {"id": 66, "name": "Preparatory Course for German Language Examinations"},
        {"id": 67, "name": "Didactics of German as a Foreign Language"},
        {"id": 68, "name": "Translation and Interpretation"},
        {"id": 69, "name": "German as a Technical Language"},
        {"id": 71, "name": "German as an Academic Language"}
    ]
}


def decode_unicode(string):
    # This pattern matches Unicode escape sequences in the form \uXXXX
    unicode_escape_pattern = re.compile(r'\\u[0-9a-fA-F]{4}')
    
    # Function to replace each Unicode escape sequence with the corresponding character
    def replace_unicode_escape(match):
        return chr(int(match.group(0)[2:], 16))
    
    # Replace Unicode escape sequences
    decoded_string = unicode_escape_pattern.sub(replace_unicode_escape, string)
    return decoded_string


def map_course_data(course):
    # Map courseType
    course_type_name = course_type_mapping.get(course.get("courseType", None), "Unknown course type")

    # Initialize subject and subSubject names and IDs
    subject_name = "Unknown subject"
    sub_subject_id = None
    sub_subject_name = "Unknown subSubject"

    # Find the matching subject and subSubject names
    for subject, sub_subjects in subject_mapping.items():
        for sub_subject in sub_subjects:
            if sub_subject["name"] == course.get("subject", ""):
                subject_name = subject
                sub_subject_id = sub_subject["id"]
                sub_subject_name = sub_subject["name"]
                break

    # Format the dates and costs
    formatted_dates = [
        {
            "start": date["start"],
            "end": date["end"],
            "costs": f"€{date['costs']}" if date.get('costs') else "Unknown",
            "registrationDeadline": date.get("registrationDeadline", "Unknown"),
            "selectHskHwk": date.get("selectHskHwk", "N/A")
        }
        for date in course.get("date", [])
    ]

    # Calculate program duration in months and total semesters
    if course.get("date"):
        start_date = course["date"][0]["start"]
        end_date = course["date"][0]["end"]
        program_duration = (int(end_date[:4]) - int(start_date[:4])) * 12 + (int(end_date[5:7]) - int(start_date[5:7]))
        total_semesters = program_duration // 6  # Assuming each semester is 6 months
    else:
        program_duration = total_semesters = 0

    # Map supportInternationalStudents to boolean
    support_international_students = course.get("supportInternationalStudents", None) is not None

    # Decode courseNameShort using the HTML unicode decoder function
    original_short_course_name = decode_unicode(course.get("courseNameShort", "Unknown Short Name"))
    original_academy = decode_unicode(course.get("academy", "Unknown Short Name"))

    # Return the transformed data
    return {
        "id": course.get("id", "Unknown ID"),
        "image": f"https://www2.daad.de{course.get('image', '')}" if course.get('image') else None,
        "programDuration": f"{program_duration} months" if program_duration else "Unknown",
        "totalSemester": total_semesters if total_semesters else 0,
        "courseName": course.get("courseName", "Unknown Course Name"),
        "courseNameShort": course.get("courseNameShort", "Unknown Course Name"),
        "originalShortCourseName": original_short_course_name,
        "academy": course.get("academy", "Unknown Academy"),
        "originalAcademy":original_academy,
        "city": course.get("city", "Unknown City"),
        "languages": course.get("languages", ["Unknown"]),
        "languageLevelGerman": course.get("languageLevelGerman","null"),
        "languageLevelEnglish": course.get("languageLevelEnglish","null"),
        "date": formatted_dates,
        "courseType": course_type_name,
        "cursorNumber": course.get("id", 1),
        "isElearning": course.get("isElearning", False),
        "applicationDeadline": course.get("applicationDeadline", "Unknown"),
        "subject": subject_name,
        "subSubjectId": sub_subject_id,
        "subSubjectName": sub_subject_name,
        "supportInternationalStudents": support_international_students,
        "link": course.get('link', ''),
        "requestLanguage": course.get("requestLanguage", "Unknown")
    }

# Load the JSON data from the file or from the API response
with open('./daad_data.json') as f:
    data = json.load(f)["courses"]  # Accessing the courses array directly

# Transform each course in the data
transformed_data = [map_course_data(course) for course in data if course]  # Skip None values

# Save the transformed data to a new JSON file
with open('./transformed_daac_data.json', 'w') as f:
    json.dump(transformed_data, f, indent=4)

print("Data transformation complete. The transformed data is saved in 'transformed_daac_data.json'.")