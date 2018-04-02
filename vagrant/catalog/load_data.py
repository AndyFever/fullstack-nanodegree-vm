from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Category, Article, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

category_one = Category(category="Tools")
session.add(category_one)
session.commit()

category_two = Category(category="Process")
session.add(category_two)
session.commit()

category_three = Category(category="Techniques")
session.add(category_three)
session.commit()

category_four = Category(category="Resources")
session.add(category_four)
session.commit()

category_five = Category(category="Technologies")
session.add(category_five)
session.commit()

category_six = Category(category="Stories")
session.add(category_six)
session.commit()

article_one = Article(parent_id=1, title="Cucumber Automation", article_text="Cucumber is a software tool used by computer programmers for testing other software. It runs automated acceptance tests written in a behavior-driven development (BDD) style. Central to the Cucumber BDD approach is its plain language parser called Gherkin. It allows expected software behaviors to be specified in a logical language that customers can understand. As such, Cucumber allows the execution of feature documentation written in business-facing text. Cucumber was originally written in the Ruby programming language and was originally used exclusively for Ruby testing as a complement to the RSpec BDD framework. Cucumber now supports a variety of different programming languages through various implementations, including Java. For example, Cuke4php and Cuke4Lua are software bridges that enable testing of PHP and Lua projects, respectively. Other implementations may simply leverage the Gherkin parser while implementing the rest of the testing framework in the target language.", owner='admin')
session.add(article_one)
session.commit()

article_two = Article(parent_id=2, title="Behavioral Driven Development", article_text="In software engineering, behavior-driven development (BDD) is a software development process that emerged from test-driven development (TDD). Behavior-driven development combines the general techniques and principles of TDD with ideas from domain-driven design and object-oriented analysis and design to provide software development and management teams with shared tools and a shared process to collaborate on software development.Although BDD is principally an idea about how software development should be managed by both business interests and technical insight, the practice of BDD does assume the use of specialized software tools to support the development process. Although these tools are often developed specifically for use in BDD projects, they can be seen as specialized forms of the tooling that supports test-driven development. The tools serve to add automation to the ubiquitous language that is a central theme of BDD", owner='admin')
session.add(article_two)
session.commit()

article_three = Article(parent_id=3, title="Equivalence Partitioning", article_text="Equivalence partitioning or equivalence class partitioning (ECP) is a software testing technique that divides the input data of a software unit into partitions of equivalent data from which test cases can be derived. In principle, test cases are designed to cover each partition at least once. This technique tries to define test cases that uncover classes of errors, thereby reducing the total number of test cases that must be developed. An advantage of this approach is reduction in the time required for testing a software due to lesser number of test cases.  Equivalence partitioning is typically applied to the inputs of a tested component, but may be applied to the outputs in rare cases. The equivalence partitions are usually derived from the requirements specification for input attributes that influence the processing of the test object.  The fundamental concept of ECP comes from equivalence class which in turn comes from equivalence relation. A software system is in effect a computable function implemented as an algorithm in some implementation programming language. Given an input test vector some instructions of that algorithm get covered, ( see code coverage for details ) others do not. This gives the interesting relationship between input test vectors:- a C b {\displaystyle _{a}C_{b}} _{a}C_{b} is an equivalence relation between test vectors a, b if and only if the coverage foot print of the vectors a, b are exactly the same, that is, they cover the same instructions, at same step. This would evidently mean that the relation cover C would partition the input vector space of the test vector into multiple equivalence class. This partitioning is called equivalence class partitioning of test input. If there are N equivalent classes, only N vectors are sufficient to fully cover the system.", owner='admin')
session.add(article_three)
session.commit()

article_four = Article(parent_id=4, title="Project Management BoK", article_text="The Project Management Body of Knowledge is a set of standard terminology and guidelines (a body of knowledge) for project management. The body of knowledge evolves over time and is presented in A Guide to the Project Management Body of Knowledge (the Guide to the PMBOK or the Guide), a book whose sixth edition was released in 2017. The Guide is a document resulting from work overseen by the Project Management Institute (PMI), which offers the CAPM and PMP certifications.", owner='admin')
session.add(article_four)
session.commit()

article_five = Article(parent_id=5, title="Restfull APIs", article_text="REpresentational State Transfer (REST) is an architectural style that defines a set of constraints and properties based on HTTP. Web Services that conform to the REST architectural style, or RESTful web services, provide interoperability between computer systems on the Internet. REST-compliant web services allow the requesting systems to access and manipulate textual representations of web resources by using a uniform and predefined set of stateless operations. Other kinds of web services, such as SOAP web services, expose their own arbitrary sets of operations.", owner='admin')
session.add(article_five)
session.commit()

article_six = Article(parent_id=6, title='Agile Testing', article_text='Agile development recognizes that testing is not a separate phase, but an integral part of software development, along with coding. Agile teams use a "whole-team" approach to "baking quality in" to the software product. Testers on agile teams lend their expertise in eliciting examples of desired behavior from customers, collaborating with the development team to turn those into executable specifications that guide coding. Testing and coding are done incrementally and interactively, building up each feature until it provides enough value to release to production.', owner='admin')
session.add(article_six)
session.commit()

article_seven = Article(parent_id=1, title="Keyword Driven Testing", article_text="Keyword-driven testing, also known as table-driven testing or action word based testing, is a software testing methodology suitable for both manual and automated testing. This method separates the documentation of test cases -including the data to use- from the prescription of the way the test cases are executed. As a result, it separates the test creation process into two distinct stages: a design and development stage, and an execution stage.", owner='admin')
session.add(article_seven)
session.commit()

article_eight = Article(parent_id=2, title="Pair Programming", article_text='Pair programming is an agile software development technique in which two programmers work together at one workstation. One, the driver, writes code while the other, the observer or navigator,[1] reviews each line of code as it is typed in. The two programmers switch roles frequently.  While reviewing, the observer also considers the "strategic" direction of the work, coming up with ideas for improvements and likely future problems to address. This is intended to free the driver to focus all of their attention on the "tactical" aspects of completing the current task, using the observer as a safety net and guide.', owner='admin')
session.add(article_eight)
session.commit()

article_nine = Article(parent_id=3, title="Boundary Analysis", article_text='Boundary value analysis is a software testing technique in which tests are designed to include representatives of boundary values in a range. The idea comes from the boundary. Given that we have a set of test vectors to test the system, a topology can be defined on that set. Those inputs which belong to the same equivalence class as defined by the equivalence partitioning theory would constitute the basis. Given that the basis sets are neighbors, there would exist a boundary between them. The test vectors on either side of the boundary are called boundary values. In practice this would require that the test vectors can be ordered, and that the individual parameters follows some kind of order (either partial order or total order).', owner='admin')
session.add(article_nine)
session.commit()

article_ten = Article(parent_id=4, title="ISTQB Guide", article_text='The International Software Testing Qualifications Board (ISTQB) is a software testing qualification certification organisation that operates internationally. Founded in Edinburgh in November 2002, ISTQB is a non-profit association legally registered in Belgium. ISTQB Certified Tester is a standardized qualification for software testers and the certification is offered by the ISTQB. The qualifications are based on a syllabus, and there is a hierarchy of qualifications and guidelines for accreditation and examination. The ISTQB is a software testing qualification certification organization having over 500,000 certifications issued; the ISTQB consists of 57 member boards worldwide representing 81 countries (date: May 2017)', owner='admin')
session.add(article_ten)
session.commit()

article_eleven = Article(parent_id=5, title="Bootstrap", article_text='Bootstrap is a free and open-source front-end library for designing websites and web applications. It contains HTML- and CSS-based design templates for typography, forms, buttons, navigation and other interface components, as well as optional JavaScript extensions. Unlike many web frameworks, it concerns itself with front-end development only.', owner='admin')
session.add(article_eleven)
session.commit()

article_twelve = Article(parent_id=6, title="From Design to Production in Minutes", article_text='Continuous delivery (CD) is a software engineering approach in which teams produce software in short cycles, ensuring that the software can be reliably released at any time.[1] It aims at building, testing, and releasing software faster and more frequently. The approach helps reduce the cost, time, and risk of delivering changes by allowing for more incremental updates to applications in production. A straightforward and repeatable deployment process is important for continuous delivery.', owner='admin')
session.add(article_twelve)
session.commit()

user_one = User(username='Dipl.-Ing. Sonya Eigenwillig MBA.', picture="http://www.galli-gentile.net/privacy.jsp", email='feijoo.nora@ferrandez.com')
session.add(user_one)
session.commit()

user_two = User(username='Dipl.-Ing. Eugenio Birnbaum', picture="http://www.taesche.com/", email='satterfield.burnett@hotmail.com')
session.add(user_two)
session.commit()
