import requests
from bs4 import BeautifulSoup

def scrap_jobs(keyword, location):
    keyword_url = keyword.replace(' ', '-').lower()
    location_url = location.replace(' ', '-').lower()
    url = f"https://id.jobstreet.com/id/{keyword_url}-jobs/in-{location_url}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Gagal Mengambil Data!")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    
    job_links = soup.find_all('a', attrs={'data-automation': 'job-list-item-link-overlay'})
    
    if not job_links:
        print("Tidak menemukan lowongan, cek struktur HTML-nya")
        return []
    
    for link in job_links:
        job_url = "https://id.jobstreet.com" + link.get('href')
        
        parent = link.parent
        
        title_tag = parent.find('h1') or parent.find('h2') or parent.find('div')
        title = title_tag.text.strip() if title_tag else 'Judul tidak ditemukan'
        

        company = 'Perusahaan tidak ditemukan'
        location = 'Lokasi tidak ditemukan'
        
        company_tag = parent.find_next('span')
        if company_tag:
            company = company_tag.text.strip()
        
        location_tag = parent.find_next('div')
        if location_tag:
            location = location_tag.text.strip()
        
        jobs.append({
            'title': title,
            'company': company,
            'location': location,
            'url': job_url
        })
    
    return jobs

if __name__ == "__main__":
    keyword = input("Masukkan jenis pekerjaan (contoh: python developer): ")
    location = input("Masukkan lokasi (contoh: jakarta): ")
    
    print(f"\nMencari lowongan untuk '{keyword}' di '{location}'...\n")
    results = scrap_jobs(keyword, location)
    
    if results:
        for idx, job in enumerate(results, 1):
            print(f"{idx}. {job['title']} - {job['company']} - {job['location']}")
    else:
        print("Tidak ada hasil yang ditemukan.")
