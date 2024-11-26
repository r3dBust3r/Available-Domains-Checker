import whois

def read_domains(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError as e:
        print(f'[!] No such file: {e}')
        exit(0)

def save_domain(file, domain):
    try:
        with open(file, '+a') as file:
            file.write(f'{domain}\n')
            file.close()
    except BaseException as e:
        print(f'[!] Failed to save domain to file\n{e}')


def check_domain_availability(domain_list):
    available_domains = []
    available_domains_file = 'available_domains.txt'

    for domain in domain_list:
        domain = domain.strip()
        try:
            # Perform a WHOIS lookup
            result = whois.whois(domain)
            # If the WHOIS result has no domain_name, it might be available
            if not result.domain_name:
                print(f"[+] {domain} is available.")
                available_domains.append(domain)
                save_domain(available_domains_file, domain)
            else:
                print(f"[-] {domain} is unavailable.")
        except whois.parser.PywhoisError:
            # WHOIS query failure indicates the domain might be available
            print(f"[+] {domain} is available.")
            available_domains.append(domain)
            save_domain(available_domains_file, domain)
        except Exception as e:
            # Handle other unexpected errors
            print(f"[!] Error checking {domain}: {e}")

    return available_domains

if __name__ == "__main__":
    domain_list_file = input('Enter the path to your domain list file: ')
    domains_to_check = read_domains(domain_list_file)
    
    available_domains = check_domain_availability(domains_to_check)
    print("\n[*] Available domains:\n")
    for domain in available_domains:
        print(f'\t[+] {domain}')
