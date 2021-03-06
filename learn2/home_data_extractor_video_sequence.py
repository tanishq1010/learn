import requests
import pandas as pd
import json
from openpyxl import Workbook, load_workbook
# from miscellaneous import *
from subject_data_extractor_video_sequence import subject_data_extractor



class Source(object):
    def __init__(self):
        super(Source, self).__init__()
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Content-Type': 'application/json; charset=UTF-8',
        }
        self.host = 'https://preprodms.embibe.com'

    def callAPI(self, url, payload, method, token):
        self.headers['embibe-token'] = token
        response = requests.request(method, self.host + url, headers=self.headers, data=payload)
        if response.status_code != 200:
            print(url + ' - ' + str(response.content))
            return None
        return response

    def main(self, child_id, board, grade, exam, goal, embibe_token):
        payload = {
            "board": goal,
            "child_id": child_id,
            "exam": exam,
            "exam_name": exam,
            "goal": goal,
            "grade": grade,
            "fetch_all_content":"true"
        }

        response1 = self.callAPI(
            f"/fiber_ms/v1/home",
            json.dumps(payload),
            'POST', embibe_token)



        # df_positive_results_all_subjects = pd.read_csv("positive_learn_results_all_subjects.csv")
        # df_negative_results_all_subjects = pd.read_csv("negative_learn_results_all_subjects.csv")



        

        for item in response1.json():
            home_data = [child_id, exam, goal,grade]
            # if item["content_section_type"] == "HEROBANNER":
            #     hero_banner_checker(response1.json(), df_negative_results_all_subjects,
            #                         df_positive_results_all_subjects, "negative_learn_results_all_subjects.csv",
            #                         "positive_learn_results_all_subjects.csv", home_data, "All Subjects")


            if item["content_section_type"] == "SUBJECTS":
                for data in item["content"]:
                    if data["subject"] == "All Subjects":
                        continue
                    else:
                       try:
                           subject_data_extractor(child_id, board, grade, exam, goal, embibe_token, data["subject"],
                                               home_data)
                       except Exception as e:
                           print(e)


            # if (item["content_section_type"] != "HEROBANNER" and item["content_section_type"] != "CONTINUELEARNING" and item["content_section_type"] != "SUBJECTS" and item[
            #     "content_section_type"] != "CONTINUELEARNING") and (
            #         item["contentType"] != "Ad_banner" and item["contentType"] != "learn_chapter"and item["section_name"] != "Embibe Explainers"and item["section_name"] != "Books With Videos & Solutions"):
            #     section_name = item["section_name"]
            #     for data in item["content"]:
            #         title = data["title"]
            #         description = data["description"]
            #         length = data["length"]
            #         currency = int(data["currency"])
            #         id = data["id"]
            #         a_string = id
            #         split_string = a_string.split("/", 1)
            #         id= split_string[0]
            #         Type = data["type"]
            #         subject_tagged = data["subject"]
            #         if title == "" or description == "" or length == "" or length == 0 or currency < 0 or id == "" or Type == "":
            #             length=minutes_converter(length)
            #             df_negative_results_all_subjects.loc[len(df_negative_results_all_subjects)] = home_data + [length, Type, id, title,section_name,currency,"All Subjects", subject_tagged,"",""]
            #             df_negative_results_all_subjects.to_csv("negative_learn_results_all_subjects.csv", index=False)
            #         else:
            #             length=minutes_converter(length)
            #             df_positive_results_all_subjects.loc[len(df_positive_results_all_subjects)] = home_data + [length, Type, id, title,section_name,currency,"All Subjects", subject_tagged,"",""]
            #             df_positive_results_all_subjects.to_csv("positive_learn_results_all_subjects.csv", index=False)

            # if (item["contentType"] == "learn_chapter"):
            #     section_name = item["section_name"]
            #     for data in item["content"]:
            #         title = data["title"]
            #         description = data["description"]
            #         # length = datta["duration"]
            #         # currency = int(data["embium_coins"])
            #         id = data["id"]
            #         a_string = id
            #         split_string = a_string.split("/", 1)
            #         id= split_string[0]

            #         Type = data["type"]
            #         subject_tagged = data["subject"]
            #         if title == "" or id == "" or Type == ""or description=="":
            #             df_negative_results_all_subjects.loc[len(df_negative_results_all_subjects)] = home_data + ["", Type, id, title,section_name,"","All Subjects", subject_tagged,"",""]
            #             df_negative_results_all_subjects.to_csv("negative_learn_results_all_subjects.csv", index=False)
            #         else:
            #             df_positive_results_all_subjects.loc[len(df_positive_results_all_subjects)] = home_data + ["", Type, id, title,section_name,"","All Subjects", subject_tagged,"",""]
            #             df_positive_results_all_subjects.to_csv("positive_learn_results_all_subjects.csv", index=False)





def home_data1(child_id, board, grade, exam, goal, embibe_token):
    src = Source()
    src.main(child_id, board, grade, exam, goal, embibe_token)


# home_data("", "", "", "", "",
#           "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic3R1ZGVudCIsInRpbWVfc3RhbXAiOiIyMDIwLTEwLTE1IDE3OjQyOjI2IFVUQyIsImlzX2d1ZXN0IjpmYWxzZSwiaWQiOjM2MTU1OTQsImVtYWlsIjoiYzEzNDEzOGUwNDc1QGppby1lbWJpYmUuY29tIn0.lG7sauHJW1Hwj3nQGzDBrBjyPbhaFJGGnZ05bbflJjkD-tmybjJ8V-Si7phyv6Wai28twrgH-J82P0iF7r_Sag")
