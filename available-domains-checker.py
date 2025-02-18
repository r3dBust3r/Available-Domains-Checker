import whois
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

def args_init():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True, help="Path to your domain-list file")
    parser.add_argument('-o', '--output', required=False, default="available_domain.txt", help="Output file")
    return parser.parse_args()

def read_domains(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError as e:
        print(f'[!] No such file: {e}')
        exit(0)

def save_domain(file, domain):
    try:
        with open(file, 'a') as file:  # Mode 'a' to append
            file.write(f'{domain}\n')
    except Exception as e:
        print(f'[!] Failed to save domain to file\n{e}')

def check_domain(domain):
    try:
        # Perform a WHOIS lookup
        result = whois.whois(domain)
        # If the WHOIS result has no domain_name, it might be available
        if not result.domain_name:
            print(f"[+] {domain} is available.")
            return domain
        else: return None
    except whois.parser.PywhoisError:
        # WHOIS query failure indicates the domain might be available
        print(f"[+] {domain} is available.")
        return domain
    except Exception as e:
        # Handle other unexpected errors
        print(f"[!] Error checking {domain}: {e}")
        return None

def check_domains_concurrently(domain_list, output_file, max_threads=20):
    available_domains = []

    with ThreadPoolExecutor(max_threads) as executor:
        future_to_domain = {executor.submit(check_domain, domain): domain for domain in domain_list}
        
        for future in as_completed(future_to_domain):
            domain = future_to_domain[future]
            try:
                result = future.result()
                if result:
                    available_domains.append(result)
                    save_domain(output_file, result)
            except Exception as e:
                print(f'[!] Exception occurred while processing {domain}: {e}')

    return available_domains

if __name__ == "__main__":

    args = args_init()
    
    domain_list_file = args.file
    domains_to_check = read_domains(domain_list_file)
    
    print("[*] Checking domain availability...")
    available_domains = check_domains_concurrently(domains_to_check, args.output)
    

    print(f'[*] Done!')
    print(f'Check your output file: {args.output}')
