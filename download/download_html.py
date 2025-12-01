import asyncio

from playwright.async_api import Browser, Page, async_playwright


def load_urls(file_path: str = "urls.txt") -> list[str]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        return []


async def download_single_html(page: Page, url: str, index: int):
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        html_content = await page.content()
        filename = f"{index}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content)
    except Exception as e:
        print(f"Error: {url} {e}")


async def main():
    urls = load_urls()
    if not urls:
        return
    async with async_playwright() as p:
        browser: Browser = await p.firefox.launch(headless=True)
        tasks = []
        for i, url in enumerate(urls):
            page: Page = await browser.new_page()
            tasks.append(download_single_html(page, url, i))
        await asyncio.gather(*tasks)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
