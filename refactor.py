import os
import re

html_file = 'layouts/index.html'
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Create directories
os.makedirs('layouts/partials', exist_ok=True)
os.makedirs('layouts/_default', exist_ok=True)
os.makedirs('content', exist_ok=True)

# Split the content
# Header: from start to end of </nav>
header_match = re.search(r'(<!DOCTYPE html>.*?</nav>)', content, re.DOTALL)
header_html = header_match.group(1) if header_match else ''

# Update navbar links in header
header_html = header_html.replace('href="#about"', 'href="/about/"')
header_html = header_html.replace('href="#services"', 'href="/services/"')
header_html = header_html.replace('href="#expertise"', 'href="/expertise/"')
header_html = header_html.replace('href="#why-us"', 'href="/why-us/"')
header_html = header_html.replace('href="#contact"', 'href="/#contact"')

# Extract sections
hero_match = re.search(r'(<!-- Hero Section -->.*?</section>)', content, re.DOTALL)
hero_html = hero_match.group(1) if hero_match else ''

about_match = re.search(r'(<!-- Vision & Mission.*?<section id="about".*?</section>)', content, re.DOTALL)
about_html = about_match.group(1) if about_match else ''

services_match = re.search(r'(<!-- Services Section -->.*?<section id="services".*?</section>)', content, re.DOTALL)
services_html = services_match.group(1) if services_match else ''

expertise_match = re.search(r'(<!-- Technology Expertise.*?<section id="expertise".*?</section>)', content, re.DOTALL)
expertise_html = expertise_match.group(1) if expertise_match else ''

why_us_match = re.search(r'(<!-- Why Us Section -->.*?<section id="why-us".*?</section>)', content, re.DOTALL)
why_us_html = why_us_match.group(1) if why_us_match else ''

benefits_match = re.search(r'(<!-- Client Benefits -->.*?</section>)', content, re.DOTALL)
benefits_html = benefits_match.group(1) if benefits_match else ''

clients_match = re.search(r'(<!-- Clients List with Better View.*?</section>)', content, re.DOTALL)
clients_html = clients_match.group(1) if clients_match else ''

# Footer: from <footer id="contact"> to </html>
footer_match = re.search(r'(<!-- Footer -->.*?</html>)', content, re.DOTALL)
footer_html = footer_match.group(1) if footer_match else ''

# Add social icons to footer
social_html = '''
            <div class="flex justify-center space-x-6 mt-8">
                <a href="#" class="text-gray-400 hover:text-accent transition">
                    <span class="sr-only">LinkedIn</span>
                    <svg class="h-8 w-8" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
                </a>
                <a href="#" class="text-gray-400 hover:text-accent transition">
                    <span class="sr-only">Twitter</span>
                    <svg class="h-8 w-8" fill="currentColor" viewBox="0 0 24 24"><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/></svg>
                </a>
            </div>
'''
footer_html = footer_html.replace('</div>\n        <div class="mt-12 text-gray-500', social_html + '\n        </div>\n        <div class="mt-12 text-gray-500')

with open('layouts/partials/header.html', 'w', encoding='utf-8') as f:
    f.write(header_html)

with open('layouts/partials/footer.html', 'w', encoding='utf-8') as f:
    f.write(footer_html)

# Create index.html for Home
new_index = f'''{{{{ partial "header.html" . }}}}
{hero_html}
{benefits_html}
{clients_html}
{{{{ partial "footer.html" . }}}}'''
with open('layouts/index.html', 'w', encoding='utf-8') as f:
    f.write(new_index)

# Create single.html for generic pages
single_html = '''{{ partial "header.html" . }}
<div class="pt-12 pb-24 bg-white">
    {{ .Content | safeHTML }}
</div>
{{ partial "footer.html" . }}'''
with open('layouts/_default/single.html', 'w', encoding='utf-8') as f:
    f.write(single_html)

# Create content files
def write_content(slug, title, html_content):
    content = f'''---
title: "{title}"
url: "/{slug}/"
---
{html_content}
'''
    with open(f'content/{slug}.md', 'w', encoding='utf-8') as f:
        f.write(content)

write_content('about', 'About Us - Vision & Mission', about_html)
write_content('services', 'Flexible Engagement Models', services_html)
write_content('expertise', 'Technology Expertise', expertise_html)
write_content('why-us', 'Why Enterprises Choose Gigworx', why_us_html)

print("Refactoring complete.")
