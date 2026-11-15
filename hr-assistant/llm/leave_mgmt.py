leave_record = []

def apply_leave(employee_id: str, start_date: str, end_date: str, leave_type: str):
    leave_record.append({
        "employee_id": employee_id,
        "start_date": start_date,
        "end_date": end_date,
        "leave_type": leave_type
    })

def list_leaves(employee_id: str):
    return [leave for leave in leave_record if leave["employee_id"] == employee_id]

def get_leave_balance(employee_id: str):
    return {
        "SICK_LEAVES": 10,
        "CASUAL_LEAVES": 5,
        "ANNUAL_LEAVES": 15
        
    }

def send_email(email_id,subject, body):
    print(f"Sending email to {email_id} with subject '{subject}' and body '{body}'")
    
def get_logged_in_employee_details():
    return {
        "name": "John Doe",
        "employee_id": "E12345",
        "department": "Engineering",
        "email_id": "john.doe@example.com",
        "manager":{
            "name" : "Jane Smith",
            "employee_id": "E54321",
            "email_id":"mahadevkv.dev@gmail.com"
        }
        
    }