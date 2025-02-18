import argparse

def args_init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help="Path to your keyword-list file separated by comma (,)")
    parser.add_argument('-o', '--output', required=False, default="domains.txt", help="Output file")
    return parser.parse_args()

def get_keywords(file):
    keywords = list()
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                for word in line.split(','):
                    word = word.lower().strip()
                    keywords.append(word.replace(' ', ''))
                    keywords.append(word.replace(' ', '-'))
                    keywords.append(word.replace(' ', '_'))
    
    except FileNotFoundError as e:
        print(f'[!] No such file {file}!')
        exit(0)

    return keywords

def generate_domains(keywords):
    domains = list()
    tlds = 'com, net, co, org, io, me, online, shop, info, dev, tech, app, tv, pro, de, at, au, be, br, ca, es, eu, fr, hu, ie, is, it, pl, uk, us'.split(', ')
    for w in keywords:
        for tld in tlds:
            domains.append(f'{w.lower().strip()}.{tld}')
    return domains

def save_domains(domains, output):
    try:
        with open(output, 'a') as file:
            for domain in domains:
                file.write(f'{domain}\n')
    except BaseException as e:
        print(f'[!] Unable to save domains {e}')
        return False
    
    return True

def main():
    args = args_init()
    keywords = get_keywords(args.file)
    domains = generate_domains(keywords)
    if save_domains(domains, args.output):
        print(f'[+] Your generated domains saved successfuly to: {args.output}')

if __name__ == '__main__':
    main()