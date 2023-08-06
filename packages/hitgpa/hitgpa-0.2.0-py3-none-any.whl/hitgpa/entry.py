from email.policy import default
from hit import score
from gpalib import convert_to_4
from gpalib.arithmetic import arithmetic
from typing import Union, Tuple, Type
import types
import pandas as pd
import argparse
from hit import ids
from hit import score



class Workable:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    @classmethod
    def from_args(cls, args, **kwargs):
        return cls.from_file(args.input_file)

    @classmethod
    def from_file(cls, input_file: str, **kwargs):
        return cls(pd.read_csv(input_file))

class Transcript(Workable):
    @staticmethod
    def from_jwes(username: Union[str, None], password: Union[str, None], test_course_only: bool = False, **kwargs) -> 'Transcript':
        def ensure_up(username: Union[str, None], password: Union[str, None]) -> Tuple[str, str]:
            if username is None or password is None:
                if username is None:
                    print('你没有通过文件输入你的成绩，必须使用学号和密码来查询，你没输学号')
                    print('你可以加上 --username [你的学号] 来解决这个问题')
                if password is None:
                    print('你没有通过文件输入你的成绩，必须使用学号和密码来查询，你没输密码')
                    print('你可以加上 --password [你的学工密码] 来解决这个问题')
                print('你也可以通过 --input [文件名]来提供你的成绩单文件')
                print('你可以通过 -h 获取一些帮助信息')
                raise ValueError
            return username, password
        username, password = ensure_up(username, password) # May raise value error here
        s = ids.idslogin(username, password)
        data = score.query(s)
        if test_course_only:
            data = data[data['是否考试课'] == '是']
        return Transcript(data)

    @classmethod
    def from_args(cls, args) -> 'Transcript':
        if args.input_file != 'jwes':
            return cls.from_file(**args.__dict__)
        else:
            return cls.from_jwes(**args.__dict__)


class Converted(Workable):
    pass
class Result(Workable):
    pass

class Factory:
    @staticmethod
    def get_type(output: str) -> Type[Workable]:
        r = {
            'transcript': Transcript,
            'converted': Converted,
            'final': Result
        }
        return r[output]

    def __init__(self, output_type: str):
        self.output = self.get_type(output_type)
        
    
    def process(self, item: Workable) -> Workable:
        if isinstance(item, self.output):
            return item
        if isinstance(item, Result):
            return item
        if isinstance(item, Transcript):
            item = Factory.convert(item)
            return self.process(item)
        if isinstance(item, Converted):
            item = Factory.fine(item)
            return self.process(item)

    @staticmethod
    def convert(item: Transcript) -> Converted:
        transcript = item.data
        converted = {}
        arith_choices = arithmetic['hundred']
        for arith in arith_choices:
            try:
                converted[arith] = convert_to_4(
                    transcript['总成绩'], score_type='hundred', arith=arith)
            except TypeError as e:
                print("我们遇到了一些问题：{}".format(str(e)))
                print("你可能需要手动清理你的“总成绩”中不是一个有效数字的地方，例如“旷考”， “取消成绩”")
                print("可以先得到CSV，再进行修改，使用--no-convert")
                print("然后使用 --input 来用文件输入数据")
                raise RuntimeError
        converted = converted
        converted['学分'] = transcript['学分'] # 让converted中有加权学分项、方便计算
        return Converted(pd.DataFrame(converted))

    @staticmethod
    def fine(item: Converted) -> Result:
        arith_choices = arithmetic['hundred']
        final_result = {}
        converted = item.data
        for arith in arith_choices:
            final_result[arith] = converted[arith].dot(
                converted['学分']) / converted['学分'].sum()
        return Result(pd.DataFrame(final_result, index=['平均学分绩']))



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-file', help='输出文件路径',
                        required=False, default='result.csv')
    parser.add_argument('-i', '--input-file',
                        help='输入成绩单文件的路径，CSV格式，如果你想通过jwes查询数据，不要使用这个参数',
                        required=False,
                        default='jwes')
    parser.add_argument('-u', '--username',
                        help='如果你想查询jwes成绩，需要提供你的学工号',
                        default=None)
    parser.add_argument('-p', '--password',
                        help='如果你想查询jwes成绩，需要提供你的学工密码',
                        default=None)

    type_help = \
"""
transcript（成绩单）
converted（四分制成绩）  
final（结果）   
"""
    input_default_type = 'transcript'
    output_default_type = 'final'
    default_type_help = '默认为 %s'
    input_type_help = '输入文件的类型' + type_help + default_type_help % (input_default_type, )
    output_help = '想要的文件类型' + type_help + default_type_help % (output_default_type, )

    type_choices = ['transcript', 'converted', 'final']

    parser.add_argument('--input-type', help=input_type_help,  choices=type_choices, default=input_default_type)
    parser.add_argument('--output-type', help=output_help, choices=type_choices, default=output_default_type)
    parser.add_argument('--test-course-only',
                        action='store_true', help='只计算考试课成绩，不计算考查课')
    # transcript --> converted --> average
    args = parser.parse_args()
    print(args.__dict__)

    factory = Factory(output_type=args.output_type)
    base = Factory.get_type(args.input_type).from_args(args)
    result = factory.process(base)
    result.data.to_csv(args.output_file)


if __name__ == '__main__':
    main()
