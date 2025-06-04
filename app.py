import requests
from bs4 import BeautifulSoup


def scrap_jobs(keyword, location):
    keyword_url = keyword.replace(" ", "-").lower()
    location_url = location.replace(" ", "-").lower()
    url = f"https://id.jobstreet.com/id/{keyword_url}-jobs/in-{location_url}"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Gagal Mengambil Data!")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    job_cards = soup.find_all("article", attrs={"data-automation": "normalJob"})
    print(f"Jumlah job cards ditemukan: {len(job_cards)}")

    jobs = []

    for card in job_cards:
        title_tag = card.find("a", attrs={"data-automation": "jobTitle"})
        company_tag = card.find("a", attrs={"data-automation": "jobCompany"})
        location_tag = card.find("a", attrs={"data-automation": "jobLocation"})

        title = title_tag.text.strip() if title_tag else "Judul tidak ditemukan"
        company = (
            company_tag.text.strip() if company_tag else "Perusahaan tidak ditemukan"
        )
        location = (
            location_tag.text.strip() if location_tag else "Lokasi tidak ditemukan"
        )

        job_url = (
            "https://id.jobstreet.com" + title_tag.get("href")
            if title_tag and title_tag.get("href")
            else "URL tidak ditemukan"
        )

        jobs.append(
            {"title": title, "company": company, "location": location, "url": job_url}
        )

    return jobs


if __name__ == "__main__":
    keyword = input("Masukkan jenis pekerjaan (contoh: python developer): ")
    location = input("Masukkan lokasi (contoh: jakarta): ")

    print(f"\nMencari lowongan untuk '{keyword}' di '{location}'...\n")
    results = scrap_jobs(keyword, location)

    if results:
        for idx, job in enumerate(results, 1):
            print(f"{idx}. {job['title']} - {job['company']} - {job['location']}")
            print(f"   Link: {job['url']}")
    else:
        print("Tidak ada hasil yang ditemukan.")
