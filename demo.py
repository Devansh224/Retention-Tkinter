import bcrypt
import datetime
from db_connection import create_connection

def seed_data():
    conn = create_connection()
    cur = conn.cursor()

    # --- Clear only demo users ---
    cur.execute("DELETE FROM users WHERE username IN (%s, %s)", ("Aarav", "Priya"))
    conn.commit()

    # --- Users ---
    users = [
        ("Aarav", "aarav@example.com", "aarav123"),
        ("Priya", "priya@example.com", "priya123")
    ]
    user_ids = []
    for username, email, password in users:
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cur.execute(
            "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
            (username, password_hash.decode("utf-8"), email)
        )
        user_ids.append(cur.lastrowid)

    # --- Subjects & Chapters ---
    subjects = {
        "Math": ["Algebra", "Geometry", "Trigonometry", "Statistics", "Probability", "Calculus", "Mensuration"],
        "Science": ["Physics", "Chemistry", "Biology", "Botany", "Zoology", "Astronomy", "Environmental Science"],
        "English": ["Grammar", "Poetry", "Prose", "Drama", "Essay Writing", "Comprehension", "Literature"],
        "History": ["Ancient India", "Medieval India", "Modern India", "World War I", "World War II", "Cold War", "Freedom Struggle"],
        "Computer Science": ["Programming", "Data Structures", "Algorithms", "Databases", "Networking", "Cyber Security", "AI Basics"],
        "Economics": ["Microeconomics", "Macroeconomics", "Supply & Demand", "GDP", "Inflation", "Trade", "Public Finance"]
    }

    subject_ids = {}
    chapter_ids = {}

    for uid in user_ids:
        chosen_subjects = ["Math", "Science", "English"] if uid == user_ids[0] else ["History", "Computer Science", "Economics"]
        subject_ids[uid] = []
        for subj in chosen_subjects:
            cur.execute("INSERT INTO subjects (user_id, name) VALUES (%s, %s)", (uid, subj))
            sid = cur.lastrowid
            subject_ids[uid].append(sid)

            # Insert 7 chapters per subject
            chapter_ids[(uid, sid)] = []
            for cname in subjects[subj]:
                cur.execute("INSERT INTO chapters (user_id, subject_id, name) VALUES (%s, %s, %s)",
                            (uid, sid, cname))
                chapter_ids[(uid, sid)].append(cur.lastrowid)

    # --- Flashcards (3–4 per chapter, due dates old) ---
    flashcards = {
        "Algebra": [
            ("Solve x² + 5x + 6", "x = -2 or -3"),
            ("Quadratic formula?", "(-b ± √(b² - 4ac)) / 2a"),
            ("Factorize x² - 9", "(x - 3)(x + 3)"),
            ("Define polynomial", "Expression with variables & coefficients"),
            ("Solve 3x - 7 = 11", "x = 6"),
            ("What is a linear equation?", "Equation of degree 1"),
            ("a² - b² formula?", "(a - b)(a + b)")
        ],

        "Geometry": [
            ("Sum of angles in triangle?", "180°"),
            ("Define parallel lines", "Lines that never meet"),
            ("Area of circle?", "πr²"),
            ("Types of triangles?", "Scalene, isosceles, equilateral"),
            ("Define radius", "Distance from center to circle"),
            ("Pythagoras theorem?", "a² + b² = c²"),
            ("Circumference formula?", "2πr")
        ],

        "Trigonometry": [
            ("sin²θ + cos²θ = ?", "1"),
            ("tanθ = ?", "sinθ / cosθ"),
            ("Value of sin90°?", "1"),
            ("Value of cos0°?", "1"),
            ("Define trigonometry", "Study of triangles & ratios"),
            ("tan45° =", "1"),
            ("sin0° =", "0")
        ],

        "Physics": [
            ("Newton's 2nd Law?", "F = ma"),
            ("Unit of force?", "Newton"),
            ("Speed formula?", "Distance ÷ Time"),
            ("Power formula?", "Work ÷ Time"),
            ("Acceleration unit?", "m/s²"),
            ("Define inertia", "Resistance to change in motion"),
            ("Unit of energy?", "Joule")
        ],

        "Chemistry": [
            ("Symbol of water?", "H₂O"),
            ("Atomic number of Oxygen?", "8"),
            ("Define acid", "Proton donor"),
            ("pH below 7?", "Acidic"),
            ("CO₂ name?", "Carbon dioxide"),
            ("NaCl name?", "Sodium chloride"),
            ("Define catalyst", "Substance that speeds reaction")
        ],

        "Biology": [
            ("Photosynthesis equation?", "6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂"),
            ("Cell is basic unit of?", "Life"),
            ("Human blood groups?", "A, B, AB, O"),
            ("Largest organ?", "Skin"),
            ("Powerhouse of cell?", "Mitochondria"),
            ("Define tissue", "Group of similar cells"),
            ("DNA stands for?", "Deoxyribonucleic Acid")
        ],

        "Grammar": [
            ("Synonym of happy?", "Joyful"),
            ("Antonym of hot?", "Cold"),
            ("Define noun", "Name of a person/place/thing"),
            ("Define verb", "Action word"),
            ("Adjective meaning?", "Describes a noun"),
            ("Plural of child?", "Children"),
            ("Opposite of give?", "Take")
        ],

        "Poetry": [
            ("Poet of 'Daffodils'?", "William Wordsworth"),
            ("Define stanza", "Group of lines in poem"),
            ("Rhyme scheme ABAB?", "Alternate rhyme"),
            ("What is metaphor?", "Indirect comparison"),
            ("Who wrote 'The Raven'?", "Edgar Allan Poe"),
            ("Define poet", "Writer of poetry"),
            ("Simile example?", "As brave as a lion")
        ],

        "History": [
            ("Year of World War II?", "1939–1945"),
            ("Leader of Quit India Movement?", "Mahatma Gandhi"),
            ("First President of India?", "Dr. Rajendra Prasad"),
            ("Who discovered America?", "Christopher Columbus"),
            ("When did WWI start?", "1914"),
            ("Indian Independence year?", "1947"),
            ("Define civilization", "Advanced human society")
        ],

        "Programming": [
            ("What is recursion?", "Function calling itself"),
            ("Python keyword for function?", "def"),
            ("Loop that runs until false?", "while loop"),
            ("What is variable?", "Container for a value"),
            ("What is IDE?", "Integrated Development Environment"),
            ("Python list symbol?", "[]"),
            ("Define algorithm", "Step-by-step solution")
        ],

        "Economics": [
            ("Define GDP", "Gross Domestic Product"),
            ("Law of demand?", "Price↑ → Demand↓"),
            ("Inflation meaning?", "Rise in general price level"),
            ("Define market", "Place for buying & selling"),
            ("Define monopoly", "One seller, many buyers"),
            ("Define supply", "Quantity producers offer"),
            ("Capital meaning?", "Man-made resources")
        ]
    }

    old_due_date = datetime.datetime.now() - datetime.timedelta(days=7)  # 1 week ago

    for (uid, sid), cids in chapter_ids.items():
        for cid in cids:
            # Get chapter name
            cur.execute("SELECT name FROM chapters WHERE id=%s", (cid,))
            cname = cur.fetchone()[0]
            if cname in flashcards:
                for front, back in flashcards[cname]:
                    cur.execute(
                        """INSERT INTO flashcards 
                           (user_id, subject_id, chapter_id, front, back, tags, next_review_date, review_interval)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (uid, sid, cid, front, back, "definition", old_due_date, 1)
                    )

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database seeded with structured demo data (3–4 flashcards per chapter, all due today)!")

if __name__ == "__main__":
    seed_data()
