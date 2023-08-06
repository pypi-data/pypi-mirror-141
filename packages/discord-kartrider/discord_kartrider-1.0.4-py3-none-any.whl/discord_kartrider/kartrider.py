from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
import discord, requests, re, nextcord

async def kartideruser(ctx, api_key, name, file=None, version=None):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    if file==None:
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Chrome(file, options=options)
    driver.get(f"https://bazzi.gg/rider/{name}")
    ranking = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[3]/div[2]/div/div/div[2]/div/p[2]'))).text
    many_track = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[3]/div[2]/div/div/div[3]/div/p[2]'))).text
    many_drive = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[3]/div[2]/div/div/div[4]/div/p[2]'))).text
    winningrate = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[3]/div[2]/div/div/div[1]/div/p[2]'))).text
    winner=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[3]/div[2]/div/div/div[1]/div/p[3]/span[1]'))).text
    loseing=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[3]/div[2]/div/div/div[1]/div/p[3]/span[2]'))).text
    licensestext=WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[1]/nav/div/div[2]/div/div[2]/span'))).text
    respone = requests.get(f"https://api.nexon.co.kr/kart/v1.0/users/nickname/{name}", headers={'Authorization': api_key})
    ids = respone.json()["accessId"]
    level = respone.json()["level"]
    driver.get(f"https://tmi.nexon.com/kart/user?nick={name}")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]/div[1]/div[2]/div[2]/div[2]/span[1]'))).click()
    licenses = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]/div[1]/div[2]/div[2]/h1/span'))).value_of_css_property("background-image")
    image = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="inner"]/div[1]/div[2]/div[1]/img'))).get_attribute('src')
    driver.quit()
    if version==None:
        embed = discord.Embed(title="카트 유저검색",description=f"{name}님의 라이더 정보", color=0x00FFFF)
        embed.add_field(name="고유 ID", value=ids, inline=True)
        embed.add_field(name="라이센스", value=licensestext, inline=True)
        embed.add_field(name="레벨", value=f"{level} 레벨", inline=True)
        embed.add_field(name="종합 승률", value=f'{winningrate}\n{str(winner)}승 {str(loseing)}패', inline=True)
        embed.add_field(name="평균 순위", value=ranking, inline=True)
        embed.add_field(name="가장 많이 플레이한 트랙", value=many_track, inline=True)
        embed.add_field(name="가장 많이 사용한 카트바디", value=many_drive, inline=True)
        embed.set_thumbnail(url=re.split('[()]',licenses)[1].strip('""'))
        embed.set_image(url=image)
        await ctx.send(embed=embed)
    else:
        embed = version.Embed(title="카트 유저검색",description=f"{name}님의 라이더 정보", color=0x00FFFF)
        embed.add_field(name="고유 ID", value=ids, inline=True)
        embed.add_field(name="라이센스", value=licensestext, inline=True)
        embed.add_field(name="레벨", value=f"{level} 레벨", inline=True)
        embed.add_field(name="종합 승률", value=f'{winningrate}\n{str(winner)}승 {str(loseing)}패', inline=True)
        embed.add_field(name="평균 순위", value=ranking, inline=True)
        embed.add_field(name="가장 많이 플레이한 트랙", value=many_track, inline=True)
        embed.add_field(name="가장 많이 사용한 카트바디", value=many_drive, inline=True)
        embed.set_thumbnail(url=re.split('[()]',licenses)[1].strip('""'))
        embed.set_image(url=image)
        await ctx.send(embed=embed)
