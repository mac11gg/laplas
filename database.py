import sqlite3

DB = 'learning.db'

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    # plans & progress
    cursor.execute('CREATE TABLE IF NOT EXISTS plans (id INTEGER PRIMARY KEY, day INTEGER, topic TEXT, materials TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS progress (id INTEGER PRIMARY KEY, plan_id INTEGER, status TEXT DEFAULT "pending")')
    # topic tables
    topics = {
        'topics_sql': [
            ('Основи SQL','https://www.w3schools.com/sql/sql_intro.asp'),
            ('Запити SELECT','https://www.w3schools.com/sql/sql_select.asp'),
            ('Фільтрація даних','https://www.w3schools.com/sql/sql_where.asp'),
            ('JOIN-операції','https://www.w3schools.com/sql/sql_join.asp'),
            ('Агрегатні функції','https://www.w3schools.com/sql/sql_count_avg_sum.asp'),
            ('Індекси та оптимізація','https://www.postgresql.org/docs/current/indexes.html'),
            ('Транзакції','https://www.w3schools.com/sql/sql_transaction.asp'),
            ('Підзапити','https://www.w3schools.com/sql/sql_subqueries.asp')
        ],
        'topics_python': [
            ('Синтаксис Python','https://docs.python.org/3/tutorial/introduction.html'),
            ('Функції в Python','https://docs.python.org/3/tutorial/controlflow.html#defining-functions'),
            ('Модулі та пакети','https://docs.python.org/3/tutorial/modules.html'),
            ('Обробка виключень','https://docs.python.org/3/tutorial/errors.html'),
            ('Колекції','https://docs.python.org/3/tutorial/datastructures.html'),
            ('File I/O','https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files'),
            ('List Comprehension','https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions'),
            ('Генератори','https://docs.python.org/3/howto/functional.html#generator-expressions')
        ],
        'topics_network': [
            ('Модель OSI','https://en.wikipedia.org/wiki/OSI_model'),
            ('TCP/IP','https://en.wikipedia.org/wiki/Internet_protocol_suite'),
            ('Маршрутизація','https://en.wikipedia.org/wiki/Routing'),
            ('Firewall','https://en.wikipedia.org/wiki/Firewall_(computing)'),
            ('DNS','https://en.wikipedia.org/wiki/Domain_Name_System'),
            ('DHCP','https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol'),
            ('VLAN','https://en.wikipedia.org/wiki/Virtual_LAN'),
            ('VPN','https://en.wikipedia.org/wiki/Virtual_private_network')
        ],
        'topics_security': [
            ('Шифрування','https://uk.wikipedia.org/wiki/Шифрування'),
            ('IDS/IPS','https://owasp.org/www-project-top-ten/'),
            ('Аутентифікація','https://en.wikipedia.org/wiki/Authentication'),
            ('Авторизація','https://en.wikipedia.org/wiki/Authorization'),
            ('SSL/TLS','https://en.wikipedia.org/wiki/Transport_Layer_Security'),
            ('Hash-функції','https://en.wikipedia.org/wiki/Cryptographic_hash_function'),
            ('Безпека API','https://owasp.org/www-project-api-security/'),
            ('XSS/CSRF','https://owasp.org/www-community/attacks/csrf')
        ],
        'topics_web': [
            ('HTML5','https://developer.mozilla.org/en-US/docs/Web/HTML'),
            ('CSS3','https://developer.mozilla.org/en-US/docs/Web/CSS'),
            ('JavaScript','https://developer.mozilla.org/en-US/docs/Web/JavaScript'),
            ('DOM','https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model'),
            ('AJAX','https://developer.mozilla.org/en-US/docs/Web/Guide/AJAX'),
            ('Responsive Design','https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design'),
            ('Web Accessibility','https://developer.mozilla.org/en-US/docs/Web/Accessibility'),
            ('Web Performance','https://developer.mozilla.org/en-US/docs/Web/Performance')
        ],
        'topics_devops': [
            ('Docker','https://docs.docker.com/get-started/'),
            ('CI/CD','https://en.wikipedia.org/wiki/CI/CD'),
            ('Моніторинг','https://prometheus.io/docs/introduction/overview/'),
            ('Terraform','https://www.terraform.io/intro/index.html'),
            ('Kubernetes','https://kubernetes.io/docs/home/'),
            ('Ansible','https://docs.ansible.com/ansible/latest/index.html'),
            ('Jenkins','https://www.jenkins.io/doc/'),
            ('GitOps','https://www.gitops.tech/')
        ],
        'topics_ai': [
            ('Основи нейромереж','https://en.wikipedia.org/wiki/Neural_network'),
            ('Машинне навчання','https://en.wikipedia.org/wiki/Machine_learning'),
            ('TensorFlow','https://www.tensorflow.org/learn'),
            ('PyTorch','https://pytorch.org/tutorials/'),
            ('Scikit-learn','https://scikit-learn.org/stable/tutorial/index.html'),
            ('Кластеризація','https://en.wikipedia.org/wiki/Cluster_analysis'),
            ('Класифікація','https://en.wikipedia.org/wiki/Statistical_classification'),
            ('Рекомендаційні системи','https://en.wikipedia.org/wiki/Recommender_system')
        ]
    }
    for tbl, items in topics.items():
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {tbl} (id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT, materials TEXT)')
        cursor.execute(f'SELECT COUNT(*) FROM {tbl}')
        if cursor.fetchone()[0] == 0:
            for topic, url in items:
                cursor.execute(f'INSERT INTO {tbl}(topic, materials) VALUES(?,?)', (topic, url))
    conn.commit()
    conn.close()

def get_tables():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'topics_%'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def save_plan(plan):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM plans')
    cursor.execute('DELETE FROM progress')
    for item in plan:
        cursor.execute('INSERT INTO plans(day, topic, materials) VALUES(?,?,?)', (item['№'], item['Тема'], item['Матеріали']))
    conn.commit()
    conn.close()

def load_plan():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('SELECT day, topic, materials FROM plans ORDER BY day')
    rows = cursor.fetchall()
    conn.close()
    return [{'№':r[0],'Тема':r[1],'Матеріали':r[2]} for r in rows]

def mark_done(day):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM plans WHERE day=?',(day,))
    pid = cursor.fetchone()[0]
    cursor.execute('INSERT OR REPLACE INTO progress(plan_id, status) VALUES (?, "done")',(pid,))
    conn.commit()
    conn.close()

def load_progress():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.day, p.topic, COALESCE((SELECT status FROM progress WHERE plan_id=p.id),"pending")
        FROM plans p ORDER BY p.day
    ''')
    rows = cursor.fetchall()
    conn.close()
    total = len(rows); done = sum(1 for r in rows if r[2]=="done")
    percent = int(done/total*100) if total else 0
    return percent, [{'№':r[0],'Тема':r[1],'Статус':r[2]} for r in rows]
