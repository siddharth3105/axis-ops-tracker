"""
Standalone seed script - run from project root with:
  .\venv\Scripts\python.exe seed.py
"""
import os, sys, random
from datetime import datetime, timedelta

# Make sure the project root is on the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.models.employee import Employee, Performance, Payment, Attendance

SUPERVISORS = ['Rishi', 'Manoj Patel', 'Arshid', 'Gobinda', 'Baba', 'Chandu', 'Vinod']
SHIFTS      = ['Full Time', 'Day Shift', 'Night Shift']
WEEKDAYS    = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
SITES       = ['Site A', 'Site B', 'Site C', 'Site D']

# Real employees from the spreadsheet
REAL_EMPLOYEES = [
    ("AX0001","Rishi Ranjan Dash","rishi.dash@awign.com","9692605419","Full Time",None,"Rishi",True,True),
    ("AX0003","L.P. Linus","lakklplbros@gmail.com","9392356996","Full Time",None,"Manoj Patel",True,False),
    ("AX0008","Aman kumar","amankumarid007@gmail.com","9660156777","Full Time",None,"Manoj Patel",True,False),
    ("AX0009","Manabbar hasan","manwar786ansari99@gmail.com","9279171712","Full Time",None,"Manoj Patel",True,False),
    ("AX0010","Rohit Gondhali","rohitgondhali05@gmail.com","9561286474","Full Time",None,"Manoj Patel",True,False),
    ("AX0011","Muneeb Ahmad Lone","lonemuneeb161@gmail.com","8899361673","Full Time",None,"Manoj Patel",True,False),
    ("AX0016","koushik b","kowshikowshik17@gmail.com","8431427231","Full Time",None,"Arshid",True,False),
    ("AX0017","babureddy konkala","babureddy950@gmail.com","9581912482","Full Time",None,"Arshid",True,False),
    ("AX0018","T darshan","tdarshantdacchu@email.com","9019325899","Full Time",None,"Arshid",True,False),
    ("AX0019","shahid alam","shahidalam951018@gmail.com","7506651691","Full Time",None,"Arshid",True,False),
    ("AX0020","Satyajit Samantaray","satyajitsamantaray2003@gmail.com","7847082477","Full Time",None,"Gobinda",True,False),
    ("AX0021","Sharvan kumar","sajankumar72524@gmail.com","6202878253","Full Time",None,"Gobinda",True,False),
    ("AX0022","Abhinash Singh Jadoun","abhinashjadoun891@gmail.com","9352981721","Full Time",None,"Gobinda",True,False),
    ("AX0023","Sajit Uddin","Sajituddin13@gmail.com","7606012533","Full Time",None,"Gobinda",True,False),
    ("AX0024","Gobinda Rakshit","gobindarakshit613@gmail.com","8917555832","Full Time",None,"Gobinda",True,True),
    ("AX0025","Saranjeet Singh","sharanjeetsinghs302@gmail.com","8792218732","Full Time","Sunday","Baba",True,False),
    ("AX0026","Venu U","venu4456@gmail.com","8008699528","Full Time","Sunday","Baba",True,False),
    ("AX0027","Snehashis Sahas","snehashis83@gmail.com","8513902838","Full Time","Sunday","Baba",True,False),
    ("AX0028","Prameed","prameedchinnamuni@gmail.com","6303278752","Full Time","Sunday","Baba",True,False),
    ("AX0029","Manoj Narsayolla","manojnarsayollaoo8@gmail.com","7780792315","Full Time",None,"Manoj Patel",True,True),
    ("AX0030","Chandu Bathini","bathinichandu636@gmail.com","9502257225","Full Time",None,"Chandu",True,True),
    ("AX0031","Baba Shaik","shaikbaba8@gmail.com","9505350374","Full Time",None,"Baba",True,True),
    ("AX0032","Shubam Chakraborty","shubamchakraborty12@gmail.com","8730026671","Full Time","Sunday","Chandu",True,False),
    ("AX0033","Rajesh Sarkar","rjshsrkr99@gmail.com","6009275157","Full Time","Sunday","Chandu",True,False),
    ("AX0034","Sujit Barlat","sujit32@gmail.com","8638205978","Full Time","Sunday","Chandu",True,False),
    ("AX0035","Sivaramakrishna","sivaramak698@gmail.com","9959262518","Full Time","Sunday","Chandu",True,False),
    ("AX0036","Bharmal rav","bharmalraosewki.com@gmail.com","6377419324","Full Time","Sunday","Chandu",True,False),
    ("AX0037","Akash P Nair","akash.nair@awign.com","8943197260","Full Time","Sunday","Baba",True,True),
    ("AX0038","Vaibhav chandrakar","vaibhav.chandrakar@awign.com","9685666924","Full Time","Sunday","Chandu",True,True),
    ("AX0039","Manoj kumar M","manoj.kumar@awign.com","8660575958","Full Time","Sunday","Gobinda",True,True),
    ("AX0040","vishal reddy","vishal.narahare@awign.com","9380895784","Full Time","Sunday","Arshid",True,True),
    ("AX0041","Om prakash","jaatanakit@gmail.com","6376302955","Full Time","Sunday","Vinod",True,False),
    ("AX0042","SURAJ SHRIVAS","suraj.shrivas@awign.com","7987032003","Full Time","Sunday","Baba",True,True),
    ("AX0043","Arshid ahmad mir","arrubhai977@gmail.com","6005566134","Full Time",None,"Arshid",True,True),
    ("AX0044","Vinod","vikasgolla121@gmail.com","9573704159","Full Time",None,"Vinod",True,True),
    ("AX0045","Ajay D","jaydubba1224@gmail.com","6300283297","Full Time",None,"Chandu",True,True),
    ("AX0046","Kota Vivek","vivekkota05@gmail.com","9346499362","Full Time","Sunday","Vinod",False,False),
    ("AX0047","Vasanth Dasarapu","dasarapuvasanth@gmail.com","9381248964","Full Time","Sunday","Vinod",False,False),
    ("AX0048","Allakonda Adarsh","allakondaadarsh456@gmail.com","8106879747","Full Time","Sunday","Vinod",False,False),
    ("AX0049","Labhishetty Shreyas","shreyaslabhishetty@gmail.com","7780452342","Full Time","Sunday","Vinod",False,False),
    ("AX0054","Molleti Satyanarayana","satya007c@gmail.com","7569508087","Day Shift","Sunday","Baba",False,False),
    ("AX0055","D Ajay","ajay.dubba@awign.com","6300283291","Day Shift","Sunday","Chandu",True,True),
    ("AX0056","narasimha naidu","naidunarasimhulu612@gmail.com","9391566713","Full Time",None,"Arshid",True,True),
]

def run():
    app = create_app()
    with app.app_context():
        print("\n" + "="*55)
        print("  AXIS OPS TRACKER - DATABASE SEED")
        print("="*55)

        # Clear existing
        print("\n[1/5] Clearing existing data...")
        Attendance.query.delete()
        Payment.query.delete()
        Performance.query.delete()
        Employee.query.delete()
        db.session.commit()
        print("      Done.")

        # Insert real employees from spreadsheet
        print("[2/5] Inserting real employees from your spreadsheet...")
        emp_objects = []
        base_date = datetime(2024, 1, 1)
        for i, row in enumerate(REAL_EMPLOYEES):
            emp_id, name, email, mobile, shift, weekoff, supervisor, resident, is_sup = row
            join_date = (base_date + timedelta(days=random.randint(0, 400))).date()
            e = Employee(
                employee_id=emp_id, name=name, email=email, mobile=mobile,
                shift=shift, weekoff_day=weekoff, supervisor=supervisor,
                status='Active',
                is_resident=resident, is_supervisor=is_sup,
                supervisor_email=f"{supervisor.lower().replace(' ','')[:8]}@awign.com",
                work_site=random.choice(SITES),
                date_of_joining=join_date,
                accommodation='Provided' if resident else 'Self',
                accommodation_status='Active',
                training_date=(join_date + timedelta(days=7)),
            )
            db.session.add(e)
            emp_objects.append(e)
        db.session.commit()
        print(f"      {len(emp_objects)} employees inserted.")

        # Performance
        print("[3/5] Creating performance records...")
        for e in emp_objects:
            days = (datetime.now().date() - e.date_of_joining).days if e.date_of_joining else 180
            db.session.add(Performance(
                employee_id=e.id,
                total_days_worked=days,
                total_production_hours=round(random.uniform(200, 1800), 2),
                quality_percentage=round(random.uniform(72, 99), 2),
                total_videos=random.randint(80, 900),
            ))
        db.session.commit()
        print("      Done.")

        # Payments
        print("[4/5] Creating payment records...")
        for e in emp_objects:
            for _ in range(random.randint(1, 4)):
                pay_date = (datetime.now() - timedelta(days=random.randint(10, 200))).date()
                db.session.add(Payment(
                    employee_id=e.id,
                    payment_date=pay_date,
                    hours_processed=round(random.uniform(40, 200), 2),
                    amount_transferred=round(random.uniform(8000, 45000), 2),
                    last_payment_date=pay_date,
                    payment_status=random.choice(['Completed','Completed','Completed','Pending','Processing']),
                ))
        db.session.commit()
        print("      Done.")

        # Attendance (last 30 days)
        print("[5/5] Creating attendance records...")
        today = datetime.now().date()
        for e in emp_objects:
            for d in range(30):
                day = today - timedelta(days=d)
                if e.date_of_joining and day < e.date_of_joining:
                    continue
                if random.random() > 0.15:
                    db.session.add(Attendance(
                        employee_id=e.id, date=day,
                        status='Present',
                        hours_worked=round(random.uniform(7, 10), 2),
                    ))
        db.session.commit()
        print("      Done.")

        # Summary
        print("\n" + "="*55)
        print("  SEED COMPLETE")
        print("="*55)
        print(f"  Employees  : {Employee.query.count()}")
        print(f"  Active     : {Employee.query.filter_by(status='Active').count()}")
        print(f"  Performance: {Performance.query.count()}")
        print(f"  Payments   : {Payment.query.count()}")
        print(f"  Attendance : {Attendance.query.count()}")
        print("="*55)
        print("\n  Run:  .\\venv\\Scripts\\python.exe run.py")
        print("  Open: http://localhost:5000\n")

if __name__ == '__main__':
    run()
