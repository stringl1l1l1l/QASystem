import sys

from django.core import serializers

from StudentQA.models import Course, Student

sys.path.append('../')
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '1'
import json

from QASystem.utils.Bert_sim.bert.run_similarity import BertSim
import tensorflow as tf

from jieba import analyse
from django.db.models import Q


class QA(object):
    def __init__(self):
        self.sim = BertSim()
        self.sim.set_mode(tf.estimator.ModeKeys.PREDICT)
        self.kinds = []
        with open("QASystem/utils/Bert_sim/bert/type.txt", 'r', encoding='utf-8') as f:
            for line in f.read().splitlines():
                self.kinds.append(line)

        self.names = []
        with open("QASystem/utils/Bert_sim/bert/name.txt", 'r', encoding='utf-8') as f:
            for line in f.read().splitlines():
                self.names.append(line)

        self.courses = []
        with open("QASystem/utils/Bert_sim/bert/course.txt", 'r', encoding='utf-8') as f:
            for line in f.read().splitlines():
                self.courses.append(line)

        # EXCEL

    def Course2Json(self, courses):
        return json.dumps(
            {
                "title": courses.title,
                "time": courses.time,
                "content": courses.content,
                "teacher": courses.teacher
            },
            ensure_ascii=False
        )

    def Stu2Json(self, student):
        return json.dumps(
            {
                "name": student.name,
                "number": student.number,
                "work": student.work,
                "attendance": student.attendance
            },
            ensure_ascii=False
        )

    def del_name(self, q, lists):
        for item in lists:
            if q.count(item):
                q = q.replace(item, '')
        return q

    def to_teacher(self, name):
        res = name
        if name == "叶老师":
            res = "叶恺翔"
        elif name == "徐老师":
            res = "徐云龙"
        elif name == "饶老师":
            res = "饶淑梅"
        elif name == "管老师":
            res = "管凯捷"
        elif name == "钱老师":
            res = "钱冀彬"
        return res

    def to_course(self, name):
        res = name

        if name == "大数据" or name == "hadoop":
            res = "《大数据开发技术hadoop》"
        elif name == "python":
            res = "《python基础》"
        elif name == "产品":
            res = "《产品浅谈》"
        elif name == "大作业":
            res = "大作业"
        elif name == "前端":
            res = "《前端开发基础》"
        else:
            res = "《机器学习入门》"
        return res

    def get_simi(self, q, lists):
        res = ''
        score = 0
        for line in lists:
            s = self.sim.predict(line, q)[0][1] + self.sim.predict(q, line)[0][1]
            # s = self.sim.predict(q, line)[0][1]
            # s = self.sim.predict(line, q)[0][1]
            if s > score:
                score = s
                res = line
        return res, score

    def get_name(self, q, lists):
        res = "null"
        for item in lists:
            if q.count(str(item)):
                res = item
        return res

    def get_jieba(self, q, lists):
        # 引入TF-IDF关键词抽取接口
        tfidf = analyse.extract_tags
        # 基于TF-IDF算法进行关键词抽取
        keywords = tfidf(q)
        # 分析抽取出的关键词
        ss = 0
        rr = ''
        for keyword in keywords:
            print(keyword)
            r, s = self.get_simi(keyword, lists)
            if s > ss:
                ss = s
                rr = r
        return rr, ss

    def get_ans(self, question):
        r2 = self.get_name(question, self.names)
        r3, s3 = self.get_simi(question, self.courses)
        # sb英文
        if question.count("python"):
            r3 = "python"

        s3 = str(s3)
        r3 = self.to_course(r3)
        r2 = self.to_teacher(r2)
        print("r3 " + r3)
        print("r2 " + r2)
        res = {}
        if r2 == "null":
            r1, s1 = self.get_simi(self.del_name(question, self.courses), self.kinds[8:])
            s1 = str(s1)

            if self.kinds[8:9].count(r1):
                res["question"] = r3 + "的上课时间？"
                res["similarity"] = s1
                # from r3 select 时间 （表2）
                courses = Course.objects.filter(
                    Q(title__exact=r3) | Q(teacher__exact=r3) | Q(content__exact=r3) | Q(time__exact=r3))
                course_list = []
                for course in courses:
                    # course_list.append(self.Course2Json(course))
                    # course_list.append(json.dumps({"time": course.time}, ensure_ascii=False))
                    course_list.append(course.time)
                res['answers'] = course_list[0]

            elif self.kinds[9:12].count(r1):
                res["question"] = r3 + "的任课老师？"
                res["similarity"] = s1
                # from r3 select 老师 （表2）
                courses = Course.objects.filter(
                    Q(title__exact=r3) | Q(teacher__exact=r3) | Q(content__exact=r3) | Q(time__exact=r3))
                course_list = []
                for course in courses:
                    # course_list.append(self.Course2Json(course))
                    # course_list.append(json.dumps({"teacher": course.teacher}, ensure_ascii=False))
                    course_list.append(course.teacher)
                res['answers'] = course_list[0]

            else:
                res["question"] = r3 + "的课程内容"
                res["similarity"] = s1
                # from r3 select 内容 （表2）
                courses = Course.objects.filter(
                    Q(title__exact=r3) | Q(teacher__exact=r3) | Q(content__exact=r3) | Q(time__exact=r3))
                course_list = []
                for course in courses:
                    # course_list.append(self.Course2Json(course))
                    # course_list.append(json.dumps({"content": course.content}, ensure_ascii=False))
                    course_list.append(course.content)
                res['answers'] = course_list[0]

        else:
            if not self.names[:10].count(r2):
                r1, s1 = self.get_simi(self.del_name(question, self.names), self.kinds[:6])
                s1 = str(s1)
                if self.kinds[0:1].count(r1):
                    res["question"] = r2 + "的作业情况？"
                    res["similarity"] = s1
                    # from r2 select 作业
                    students = Student.objects.filter(Q(name__exact=r2) |
                                                      Q(work__exact=r2) | Q(number__exact=r2) | Q(
                        attendance__exact=r2) | Q(gender__exact=r2))
                    stu_list = []
                    for stu in students:
                        # stu_list.append(self.Stu2Json(stu))
                        # stu_list.append(json.dumps({"work": stu.work}, ensure_ascii=False))
                        stu_list.append(stu.work)
                    res['answers'] = stu_list
                elif self.kinds[1:4].count(r1):
                    res["question"] = r2 + "的签到情况？"
                    res["similarity"] = s1
                    # from r2 select 签到
                    students = Student.objects.filter(Q(name__exact=r2) |
                                                      Q(work__exact=r2) | Q(number__exact=r2) | Q(
                        attendance__exact=r2) | Q(gender__exact=r2))
                    stu_list = []
                    for stu in students:
                        # stu_list.append(self.Stu2Json(stu))
                        # stu_list.append(json.dumps({"attendance": stu.attendance}, ensure_ascii=False))
                        stu_list.append(stu.attendance)
                    res['answers'] = stu_list[0]

                elif self.kinds[4].count(r1):
                    res["question"] = r2 + "的性别？"
                    res["similarity"] = s1
                    # from r2 select 性别
                    students = Student.objects.filter(Q(name__exact=r2) |
                                                      Q(work__exact=r2) | Q(number__exact=r2) | Q(
                        attendance__exact=r2) | Q(gender__exact=r2))
                    stu_list = []
                    for stu in students:
                        # stu_list.append(self.Stu2Json(stu))
                        # stu_list.append(json.dumps({"gender": stu.gender}, ensure_ascii=False))
                        stu_list.append(stu.gender)
                    res['answers'] = stu_list[0]

                elif self.kinds[5].count(r1):
                    res["question"] = r2 + "的学号？"
                    res["similarity"] = s1
                    # from r2 select 学号
                    students = Student.objects.filter(Q(name__exact=r2) |
                                                      Q(work__exact=r2) | Q(number__exact=r2) | Q(
                        attendance__exact=r2) | Q(gender__exact=r2))
                    stu_list = []
                    for stu in students:
                        # stu_list.append(self.Stu2Json(stu))
                        # stu_list.append(json.dumps({"number": stu.number}, ensure_ascii=False))
                        stu_list.append(stu.number)
                    res['answers'] = stu_list[0]

            else:
                res["question"] = r2 + "上什么课？"
                res["similarity"] = str(1.0)
                # from r2 select 课程 （表2）
                courses = Course.objects.filter(
                    Q(title__exact=r2) | Q(teacher__exact=r2) | Q(content__exact=r2) | Q(time__exact=r2))
                course_list = []
                for course in courses:
                    # course_list.append(self.Course2Json(course))
                    # course_list.append(json.dumps({"title": course.title}, ensure_ascii=False))
                    course_list.append(course.title)
                res['answers'] = course_list[0]
        print(res['answers'])
        return res


if __name__ == '__main__':
    qa = QA()
    courses = Course.objects.raw()
    # while True:
    #     question = input("【input】:")
    #     qa.get_ans(question)
