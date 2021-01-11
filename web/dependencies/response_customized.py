from dependencies.mapping_dict_response import mapping_dict_response

class Line:
    def __init__(self, msg: str):
        self.msg = msg
    def judge_msg(self):
        customize_word_list = [i for i in mapping_dict_response]
        if self.msg in customize_word_list:
            return_word = mapping_dict_response[self.msg]
        else:
            return_word = self.msg

        return return_word
