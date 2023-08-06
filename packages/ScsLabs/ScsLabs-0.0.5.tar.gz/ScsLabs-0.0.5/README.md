# **[ScsLabs](https://pypi.org/project/ScsLabs/)** 
# ~ Alat bantu untuk para Pelajar 
# & Pengembangan
Skull Cyber Security Labs adalah 
modul Python untuk pembelajaran 
yang dapat menjalankan perintah 
pada program komputer.
## Installasi ScsLabs via PyPi
`pip install ScsLabs`
### Fitur yang tersedia saat ini:
- DNS Loockup (Whois Domain 
Loockup) 
`whois_domain("example.com")` - 
APNIC Lockup (IP Address Loockup) 
`whois_ip("ip")`
### Cara menggunakan ScsLabs
```python import ScsLabs as sl 
domain = skullcybersecurity.com
# Jika kamu ingin mencetak 
# nilainya secara langsung di 
# Terminal / IDE Python, maka 
# kamu harus menuliskan syntax 
# berikut:
data = sl.whois_domain(domain) 
print(data) ```
### Menyimpan hasil dari ScsLabs
```python import ScsLabs as sl 
domain = skullcybersecurity.com
# Jika kamu ingin menyimpan 
# nilainya kedalam file, maka 
# kamu harus menuliskan syntax 
# berikut:
data = sl.whois_domain(domain)
# Extention fileName akan secara 
# otomatis menjadi fileName.txt
save("fileName",data) ```
### Support Me with Coffee
<p><a 
href="https://www.buymeacoffee.com/scs26"> 
<img align="left" 
src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" 
height="50" width="210" 
alt="SkullCyberSecurity" 
/></a></p>
