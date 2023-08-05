__author__ = 'Andrey Komissarov'
__email__ = 'andrey.komissarov@starwind.com'
__date__ = '2021'

import argparse

from tcclient import TCRestClient

parser = argparse.ArgumentParser(
    prog='Allure report environment',
    usage='Specify all necessary parameters and have a rest while script working',
    description='This script creates <environment.properties> for the Allure report.',
    add_help=True,
    epilog='Developed by Komissarov')

parser.add_argument('-u', '--url', dest='url', help='TC full address', required=False, default='http://tc.tl.local')
parser.add_argument('-t', '--token', dest='token', help='User\'s token with necessary rights', required=True)
parser.add_argument('-p', '--project', dest='project', help='TC projects ID', required=False, default='Voodoo')
parser.add_argument('-s', '--parameter', dest='parameter', help='Parameter name', required=False,
                    default='env.cluster_ip')
parser.add_argument('-v', '--value', dest='value', help='Parameter value', required=True)

if __name__ == '__main__':
    args = parser.parse_args()

    print('=' * 25)
    print(f'Project: {args.project}')
    print(f'Parameter: {args.parameter}')
    print(f'Value: {args.value}')
    print('=' * 25)

    client = TCRestClient(args.url, args.token)
    response = client.set_project_parameter(uid=args.project, parameter=args.parameter, value=args.value)
    print(f'{response.text = }')
    print(f'{response.status_code = }')
