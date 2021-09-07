from .models import Exam, Exam_Detail, Pyqs
import json

class UPSC():

    files = [('exams/datafiles/nda.txt', 'National Defence Academy and Naval Academy Examination'), ('exams/datafiles/ies.txt', 'Indian Engineering Service Examination'), ('exams/datafiles/ifs.txt', 'Indian Forest Service Examination'), ('exams/datafiles/ies-iss.txt', 'Indian Economic Service - Indian Statistical Service Examination'), ('exams/datafiles/cms.txt', 'Combined Medical Services Examination'), ('exams/datafiles/cisf.txt', 'CISF AC (EXE) Examination'), ('exams/datafiles/cgs.txt', 'Combined Geo-Scientist & Geologist Exam'), ('exams/datafiles/cds.txt', 'Combined Defence Services Examination'), ('exams/datafiles/capf.txt', 'Central Armed Police Forces (ACs) Examination')]
    files2 = [('exams/datafiles/ies2.txt', 'Indian Engineering Service Examination'), ('exams/datafiles/civilserv.txt', 'Civil Service Examination')]

    def upsc(file_name, field):
        exam = 'UPSC'
        #newexam = Exam.objects.get_or_create(exam=exam)
        field = field
        Exam_Detail.objects.get_or_create(field = field, exam = Exam.objects.get(exam = exam))
        file = open(file_name, 'r')
        hand = file.read()
        hand = json.loads(hand)
        items = list(hand.items())
        for item in items:
            year = item[0][6:]
            print(year)
            objs = list(item[1].items())
            for k in objs:
                #print(k)
                phase = k[0]
                print(phase)
                sub = list(k[1].items())
                for s in sub:
                    subject = s[0]
                    link = s[1]
                    Pyqs.objects.get_or_create(
                        exam = Exam.objects.get(exam = exam),
                        exam_field = Exam_Detail.objects.get(field = field),
                        phase = phase,
                        year = year,
                        subject = subject,
                        link = link
                    )
                    print(subject)
                    print(link)
                print()
            print()    
            print()
            file.close()
        Pyqs.save
        Exam_Detail.save
        Exam.save

    def upsc_cat(file_name, field):
        exam = 'UPSC'
        #newexam = Exam.objects.get_or_create(exam=exam)

        field = field
        Exam_Detail.objects.get_or_create(field = field)

        file = open(file_name, 'r')
        hand = file.read()
        hand = json.loads(hand)
        items = list(hand.items())
        for item in items:
            year = item[0][6:]
            print(year)
            objs = list(item[1].items())
            for k in objs:
                #print(k)
                phase = k[0]
                print(phase)
                sub = list(k[1].items())
                for s in sub:
                    subject_category = s[0]
                    print(subject_category)
                    pyq = list(s[1].items())
                    for p in pyq:
                        subject = p[0]
                        link = p[1]
                        Pyqs.objects.get_or_create(
                            exam = Exam.objects.get(exam = exam),
                            exam_field = Exam_Detail.objects.get(field = field),
                            phase = phase,
                            year = year,
                            category = subject_category,
                            subject = subject,
                            link = link
                        )
                        print(subject)
                        print(link)
                    print()
                print()
            print()    
            print()
        file.close()
        Pyqs.save
        Exam_Detail.save
        Exam.save
        
    for k in files:
        upsc(k[0], k[1])

    for k in files2:
        upsc_cat(k[0], k[1])

    