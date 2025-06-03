import json
from playwright.async_api import async_playwright
from pathlib import Path
from . import nonebot_plugin_localstore as store

module_path: Path = store.get_plugin_data_dir()
plugin_data_file: Path = store.get_plugin_data_file("filename")

async def get_avatar_list_png(user_id):
    with open(f"{module_path}/ZZZ_data/avatar/list/{user_id}.json", 'r', encoding='utf-8') as f:
        data = json.load(f)

    ELEMENT_MAP = {
        200: "物理",
        201: "火",
        202: "冰",
        203: "电",
        205: "以太"
    }

    PROFESSION_MAP = {
        1: "强攻",
        2: "击破",
        3: "异常",
        4: "支援",
        5: "防护"
    }

    character_cards = [
                f"""
                <div class="character-card">
                    <div class="card-header">
                        <img src="{char['role_square_url']}" 
                             alt="{char['name_mi18n']}" 
                             class="character-avatar avatar-{char['rarity']}">
                        <div class="character-info">
                            <div class="character-name">{char['name_mi18n']}</div>
                            <div class="character-fullname">{char['full_name_mi18n']}</div>
                            <div class="character-details">
                                <span class="detail-badge element-badge">{ELEMENT_MAP.get(char['element_type'], '未知')}</span>
                                <span class="detail-badge profession-badge">{PROFESSION_MAP.get(char['avatar_profession'], '未知')}</span>
                                <span class="detail-badge camp-badge">{char['camp_name_mi18n']}</span>
                            </div>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="character-stats">
                            <div class="stat">
                                <div class="stat-value">Lv.{char['level']}</div>
                                <div class="stat-label">等级</div>
                            </div>
                            <div class="stat">
                                <div class="stat-value">{char['rarity']}</div>
                                <div class="stat-label">稀有度</div>
                            </div>
                            <div class="stat">
                                <div class="stat-value">{char['rank'] if char['rank'] > 0 else '0'}</div>
                                <div class="stat-label">命座</div>
                            </div>
                        </div>
                    </div>
                </div>
                """ 
                for char in sorted(data, key=lambda x: (x['rarity'], x['level']), reverse=True)
            ]
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>绝区零角色图鉴</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Microsoft YaHei', sans-serif;
            }}
            
            body {{
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                color: #e0e0ff;
                padding: 20px;
                min-height: 100vh;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
            }}
            
            header {{
                text-align: center;
                padding: 30px 0;
                margin-bottom: 30px;
                border-bottom: 2px solid #4cc9f0;
            }}
            
            h1 {{
                font-size: 2.8rem;
                background: linear-gradient(90deg, #4cc9f0, #f72585);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                letter-spacing: 2px;
                margin-bottom: 10px;
            }}
            
            .subtitle {{
                font-size: 1.2rem;
                color: #a9d6e5;
                opacity: 0.8;
            }}
            
            .stats {{
                display: flex;
                justify-content: center;
                gap: 30px;
                margin: 20px 0;
                flex-wrap: wrap;
            }}
            
            .stat-card {{
                background: rgba(25, 40, 65, 0.7);
                border-radius: 12px;
                padding: 15px 25px;
                text-align: center;
                min-width: 150px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(76, 201, 240, 0.3);
            }}
            
            .stat-value {{
                font-size: 2.2rem;
                font-weight: bold;
                color: #4cc9f0;
                margin: 5px 0;
            }}
            
            .stat-label {{
                font-size: 0.9rem;
                color: #a9d6e5;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .characters-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 25px;
                margin-top: 30px;
            }}
            
            .character-card {{
                background: rgba(30, 40, 60, 0.85);
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                backdrop-filter: blur(5px);
                border: 1px solid rgba(76, 201, 240, 0.2);
            }}
            
            .character-card:hover {{
                transform: translateY(-10px);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
                border-color: rgba(76, 201, 240, 0.5);
            }}
            
            .card-header {{
                display: flex;
                align-items: center;
                padding: 20px;
                background: rgba(20, 30, 50, 0.7);
                border-bottom: 1px solid rgba(76, 201, 240, 0.2);
            }}
            
            .character-avatar {{
                width: 80px;
                height: 80px;
                border-radius: 50%;
                object-fit: cover;
                border: 3px solid;
                margin-right: 20px;
            }}
            
            .avatar-S {{
                border-color: #f9c74f;
            }}
            
            .avatar-A {{
                border-color: #9d4edd;
            }}
            
            .character-info {{
                flex: 1;
            }}
            
            .character-name {{
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 5px;
                color: #f8f9fa;
            }}
            
            .character-details {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 8px;
            }}
            
            .detail-badge {{
                padding: 4px 10px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: 500;
            }}
            
            .element-badge {{
                background: rgba(76, 201, 240, 0.2);
                color: #4cc9f0;
            }}
            
            .profession-badge {{
                background: rgba(247, 37, 133, 0.2);
                color: #f72585;
            }}
            
            .camp-badge {{
                background: rgba(106, 76, 240, 0.2);
                color: #6a4cf0;
            }}
            
            .card-body {{
                padding: 20px;
            }}
            
            .character-stats {{
                display: flex;
                justify-content: space-between;
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .stat {{
                text-align: center;
            }}
            
            .stat-value {{
                font-size: 1.4rem;
                font-weight: bold;
                color: #4cc9f0;
            }}
            
            .stat-label {{
                font-size: 0.85rem;
                color: #a9d6e5;
                margin-top: 5px;
            }}
            
            .rank-badge {{
                position: absolute;
                top: 15px;
                right: 15px;
                width: 36px;
                height: 36px;
                background: linear-gradient(135deg, #f72585, #b5179e);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 1.1rem;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
            }}
            
            .character-card {{
                position: relative;
            }}
            
            footer {{
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                color: #a9d6e5;
                font-size: 0.9rem;
                border-top: 1px solid rgba(76, 201, 240, 0.2);
            }}
            
            @media (max-width: 768px) {{
                .characters-grid {{
                    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                }}
                
                .stats {{
                    flex-direction: column;
                    align-items: center;
                }}
                
                .stat-card {{
                    width: 100%;
                    max-width: 300px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>绝区零·角色图鉴</h1>
                <div class="subtitle">空洞探索者档案 · 机密数据</div>
                
                <div class="stats">
                    <div class="stat-card">
                        <div class="stat-value">{len(data)}</div>
                        <div class="stat-label">角色总数</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{len([c for c in data if c['rarity'] == 'S'])}</div>
                        <div class="stat-label">S级角色</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{len([c for c in data if c['level'] == 60])}</div>
                        <div class="stat-label">满级角色</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{len(set(c['camp_name_mi18n'] for c in data))}</div>
                        <div class="stat-label">所属阵营</div>
                    </div>
                </div>
            </header>
            
            <div class="characters-grid">
                {''.join(character_cards)}
            </div>
            
            <footer>
                <p>制图人：@STES沐霖韵</p>
            </footer>
        </div>
    </body>
    </html>
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            args=['--allow-file-access-from-files', '--disable-web-security']
        )
        context = await browser.new_context(
            bypass_csp=True,
        )
        page = await context.new_page()
        await page.set_content(html_content)
        await page.wait_for_load_state('networkidle')
        await page.set_viewport_size({'width': 1080, 'height': 1080})
        await page.screenshot(path=f"{module_path}/out/{user_id}.png", full_page=True)
        await browser.close()

async def get_avatar_info_png(user_id,num):
    with open(f"{module_path}/ZZZ_data/avatar/info/{user_id}.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        data = data[num]

    avatar = data['data']['avatar_list'][0]
    name = avatar['name_mi18n']
    full_name = avatar['full_name_mi18n']
    level = avatar['level']
    
    element_mapping = {
        200: "物理属性",
        201: "火属性",
        202: "冰属性",
        203: "电属性",
        205: "以太属性"
    }
    element_type = element_mapping.get(avatar['element_type'], f"属性{avatar['element_type']}")
    
    camp = avatar['camp_name_mi18n']
    rarity = avatar['rarity']
    vertical_painting_url = avatar['role_vertical_painting_url']
    rank = avatar['rank']

    properties = {p['property_name']: p['final'] for p in avatar['properties']}
    
    weapon = avatar['weapon']
    
    equipments = avatar['equip']

    skills = avatar['skills']

    ranks = avatar['ranks']
    
    skill_type_names = {
        0: "普通攻击",
        1: "特殊技",
        2: "闪避技",
        3: "终结技",
        5: "核心被动",
        6: "支援技"
    }

    suit_effects = {}
    for eq in equipments:
        suit = eq['equip_suit']
        suit_id = suit['suit_id']
        
        if suit_id not in suit_effects or suit_effects[suit_id]['own'] < suit['own']:
            suit_effects[suit_id] = {
                'name': suit['name'],
                'own': suit['own'],
                'desc1': suit['desc1'],
                'desc2': suit['desc2']
            }
    
    suit_effects_html = ""
    for suit_id, suit_info in suit_effects.items():
        if suit_info['own'] >= 2:
            suit_effects_html += f"""
            <div class="suit-effect">
                <p><strong>{suit_info['name']} (2件套)</strong></p>
                <p>{suit_info['desc1']}</p>
            </div>
            """
        if suit_info['own'] >= 4:
            suit_effects_html += f"""
            <div class="suit-effect">
                <p><strong>{suit_info['name']} (4件套)</strong></p>
                <p>{suit_info['desc2']}</p>
            </div>
            """

    if not suit_effects_html:
        suit_effects_html = "<p>未激活任何套装效果</p>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{full_name} - 角色详情</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Microsoft YaHei', sans-serif;
            }}
            
            body {{
                background: linear-gradient(135deg, #0a1929, #1a3a5f);
                color: #e0f0ff;
                padding: 20px;
                min-height: 100vh;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                display: grid;
                grid-template-columns: 300px 1fr;
                gap: 20px;
            }}
            
            .header {{
                grid-column: 1 / -1;
                text-align: center;
                padding: 20px 0;
                border-bottom: 2px solid #2a8b8b;
                margin-bottom: 20px;
            }}
            
            .character-name {{
                font-size: 36px;
                font-weight: bold;
                letter-spacing: 2px;
                text-shadow: 0 0 10px #00c8ff;
                color: #ffffff;
                margin-bottom: 5px;
            }}
            
            .character-title {{
                font-size: 20px;
                color: #a0d7ff;
                margin-bottom: 15px;
            }}
            
            .character-info {{
                display: flex;
                justify-content: center;
                gap: 20px;
                font-size: 16px;
            }}
            
            .character-info-item {{
                background: rgba(20, 50, 80, 0.7);
                padding: 8px 15px;
                border-radius: 20px;
                border: 1px solid #2a8b8b;
            }}
            
            .sidebar {{
                background: rgba(10, 30, 50, 0.8);
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 0 20px rgba(0, 150, 200, 0.3);
                border: 1px solid #2a8b8b;
                display: flex;
                flex-direction: column;
            }}
            
            .character-portrait {{
                width: 100%;
                border-radius: 15px;
                overflow: hidden;
                margin-bottom: 20px;
                border: 2px solid #2a8b8b;
            }}
            
            .character-portrait img {{
                width: 100%;
                display: block;
            }}
            
            .stats-box {{
                background: rgba(5, 25, 45, 0.7);
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
                border: 1px solid #2a8b8b;
            }}
            
            .skills-box {{
                background: rgba(5, 25, 45, 0.7);
                border-radius: 10px;
                padding: 15px;
                border: 1px solid #2a8b8b;
                margin-top: 20px; /* 确保技能区域在底部 */
            }}
            
            .stats-title, .skills-title {{
                font-size: 20px;
                color: #00c8ff;
                margin-bottom: 15px;
                text-align: center;
                padding-bottom: 8px;
                border-bottom: 1px solid #2a8b8b;
            }}
            
            .stat-item {{
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px dashed rgba(42, 139, 139, 0.5);
            }}
            
            .skill-item {{
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px dashed rgba(42, 139, 139, 0.5);
            }}
            
            .stat-name, .skill-type {{
                color: #a0d7ff;
            }}
            
            .stat-value, .skill-level {{
                font-weight: bold;
                color: #ffffff;
            }}
            
            .main-content {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }}
            
            .card {{
                background: rgba(10, 30, 50, 0.8);
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 0 20px rgba(0, 150, 200, 0.3);
                border: 1px solid #2a8b8b;
            }}
            
            .weapon-card {{
                grid-column: 1 / -1;
            }}
            
            .card-title {{
                font-size: 22px;
                color: #00c8ff;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
            }}
            
            .card-title i {{
                margin-right: 10px;
                color: #2a8b8b;
            }}
            
            .weapon-info {{
                display: flex;
                align-items: center;
                gap: 20px;
                margin-bottom: 20px;
            }}
            
            .weapon-icon {{
                width: 80px;
                height: 80px;
                border-radius: 10px;
                overflow: hidden;
                border: 2px solid #2a8b8b;
            }}
            
            .weapon-icon img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}
            
            .weapon-details {{
                flex: 1;
            }}
            
            .weapon-name {{
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 5px;
                color: #ffffff;
            }}
            
            .weapon-stats {{
                display: flex;
                gap: 20px;
                margin-top: 10px;
            }}
            
            .weapon-stat {{
                background: rgba(5, 25, 45, 0.7);
                padding: 8px 15px;
                border-radius: 8px;
            }}
            .weapon-meta {{
                display: flex;
                gap: 15px;
                margin-bottom: 10px;
                font-size: 16px;
            }}

            .weapon-rarity {{
                background: linear-gradient(45deg, #3a6186, #89253e);
                padding: 4px 12px;
                border-radius: 15px;
                color: white;
            }}

            .weapon-refinement {{
                background: linear-gradient(45deg, #8e2de2, #4a00e0);
                padding: 4px 12px;
                border-radius: 15px;
                color: white;
            }}
            
            .talent-content {{
                background: rgba(5, 25, 45, 0.7);
                padding: 15px;
                border-radius: 10px;
                line-height: 1.6;
                color: #c0e0ff;
            }}
            
            .equipment-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
            }}
            
            .equipment-item {{
                background: rgba(5, 25, 45, 0.7);
                border-radius: 10px;
                padding: 15px;
                text-align: center;
                border: 1px solid #2a8b8b;
            }}
            
            .equipment-icon {{
                width: 80px;
                height: 80px;
                margin: 0 auto 10px;
                border-radius: 10px;
                overflow: hidden;
                border: 2px solid #2a8b8b;
            }}
            
            .equipment-icon img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}
            
            .equipment-name {{
                font-weight: bold;
                margin-bottom: 8px;
                color: #ffffff;
            }}
            
            .equipment-stats {{
                font-size: 14px;
                color: #a0d7ff;
            }}
            
            .sub-properties {{
                margin-top: 10px;
                padding-top: 10px;
                border-top: 1px dashed rgba(42, 139, 139, 0.3);
                font-size: 12px;
                color: #a0d7ff;
            }}
            
            .sub-prop-item {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 3px;
            }}
            
            .rank-item {{
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 1px dashed rgba(42, 139, 139, 0.5);
            }}
            
            .rank-icon {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                flex-shrink: 0;
            }}
            
            .unlocked {{
                background: #2a8b8b;
                color: white;
            }}
            
            .locked {{
                background: #555;
                color: #999;
            }}
            
            .rank-content {{
                flex: 1;
            }}
            
            .rank-name {{
                font-weight: bold;
                margin-bottom: 5px;
            }}
            
            .unlocked-name {{
                color: #00c8ff;
            }}
            
            .locked-name {{
                color: #888;
            }}
            
            .rank-desc {{
                font-size: 14px;
                line-height: 1.5;
            }}
            
            .unlocked-desc {{
                color: #c0e0ff;
            }}
            
            .locked-desc {{
                color: #777;
            }}
            
            .footer {{
                grid-column: 1 / -1;
                text-align: center;
                padding: 20px;
                color: #5a9db8;
                font-size: 14px;
                border-top: 1px solid #2a8b8b;
                margin-top: 20px;
            }}
            
            .rarity-badge {{
                display: inline-block;
                background: linear-gradient(45deg, #6a5acd, #9370db);
                color: white;
                padding: 3px 10px;
                border-radius: 10px;
                font-size: 14px;
                margin-left: 10px;
                vertical-align: middle;
            }}
            
            .constellation-badge {{
                display: inline-block;
                background: linear-gradient(45deg, #1e3c72, #2a5298);
                color: white;
                padding: 3px 10px;
                border-radius: 10px;
                font-size: 14px;
                margin-left: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 class="character-name">{full_name}</h1>
                <div class="character-title">{name} · {camp}</div>
                <div class="character-info">
                    <div class="character-info-item">Lv.{level}</div>
                    <div class="character-info-item">{element_type}</div>
                    <div class="character-info-item">稀有度: <span class="rarity-badge">{rarity}</span></div>
                    <div class="character-info-item">命之座: <span class="constellation-badge">{rank}/6</span></div>
                </div>
            </div>
            
            <div class="sidebar">
                <div class="character-portrait">
                    <img src="{vertical_painting_url}" alt="{full_name}">
                </div>
                
                <div class="stats-box">
                    <h2 class="stats-title">角色属性</h2>
                    <div class="stat-item">
                        <span class="stat-name">生命值</span>
                        <span class="stat-value">{properties.get('生命值', 'N/A')}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-name">攻击力</span>
                        <span class="stat-value">{properties.get('攻击力', 'N/A')}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-name">防御力</span>
                        <span class="stat-value">{properties.get('防御力', 'N/A')}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-name">暴击率</span>
                        <span class="stat-value">{properties.get('暴击率', 'N/A')}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-name">暴击伤害</span>
                        <span class="stat-value">{properties.get('暴击伤害', 'N/A')}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-name">{element_type}伤害加成</span>
                        <span class="stat-value">{properties.get(element_type + '伤害加成', 'N/A')}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-name">异常掌控</span>
                        <span class="stat-value">{properties.get('异常掌控', 'N/A')}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-name">异常精通</span>
                        <span class="stat-value">{properties.get('异常精通', 'N/A')}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-name">穿透值</span>
                        <span class="stat-value">{properties.get('穿透值', 'N/A')}</span>
                    </div>
                </div>
                
                <div class="skills-box">
                    <h2 class="skills-title">技能等级</h2>
                    {''.join([f'''
                    <div class="skill-item">
                        <span class="skill-type">{skill_type_names.get(skill['skill_type'], f"技能类型{skill['skill_type']}")}</span>
                        <span class="skill-level">Lv.{skill['level']}</span>
                    </div>
                    ''' for skill in skills])}
                </div>
            </div>
            
            <div class="main-content">
                <div class="card weapon-card">
                    <h2 class="card-title"><i>⚔️</i>武器 - {weapon['name']}</h2>
                    <div class="weapon-info">
                        <div class="weapon-icon">
                            <img src="{weapon['icon']}" alt="{weapon['name']}">
                        </div>
                        <div class="weapon-details">
                            <div class="weapon-name">{weapon['name']} <span class="rarity-badge">Lv.{weapon['level']}</span></div>
                            <div class="weapon-meta">
                                <span class="weapon-rarity">等级: {weapon['rarity']}</span>
                                <span class="weapon-refinement">精炼等级: {weapon['star']}</span>
                            </div>
                            <div class="talent-content">
                                <b>{weapon['talent_title']}:</b> {weapon['talent_content']}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h2 class="card-title"><i>🛡️</i>装备</h2>
                    <div class="equipment-grid">
                        {''.join([f'''
                        <div class="equipment-item">
                            <div class="equipment-icon">
                                <img src="{eq['icon']}" alt="{eq['name']}">
                            </div>
                            <div class="equipment-name">{eq['name']}</div>
                            <div class="equipment-stats">
                                {eq['main_properties'][0]['property_name']}: {eq['main_properties'][0]['base']}
                            </div>
                            <div class="sub-properties">
                                {"".join([f'<div class="sub-prop-item"><span>{prop["property_name"]}</span><span>{prop["base"]}</span></div>' for prop in eq['properties']])}
                            </div>
                        </div>
                        ''' for eq in equipments])}
                    </div>
                    
                    <h3 style="margin-top: 20px; color: #00c8ff;">套装效果</h3>
                    <div class="talent-content">
                        {suit_effects_html}
                    </div>
                </div>
                
                <div class="card">
                    <h2 class="card-title"><i>✨</i>命之座</h2>
                    {''.join([f'''
                    <div class="rank-item">
                        <div class="rank-icon {'unlocked' if rank['is_unlocked'] else 'locked'}">{rank['pos']}</div>
                        <div class="rank-content">
                            <div class="rank-name {'unlocked-name' if rank['is_unlocked'] else 'locked-name'}">{rank['name']} {'(已解锁)' if rank['is_unlocked'] else '(未解锁)'}</div>
                            <div class="rank-desc {'unlocked-desc' if rank['is_unlocked'] else 'locked-desc'}">{rank['desc']}</div>
                        </div>
                    </div>
                    ''' for rank in ranks])}
                </div>
            </div>
            
            <div class="footer">
                <p>绝区零 · {full_name}角色详情面板 | 制作人@STES沐霖韵</p>
            </div>
        </div>
    </body>
    </html>
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            args=['--allow-file-access-from-files', '--disable-web-security']
        )
        context = await browser.new_context(
            bypass_csp=True,
        )
        page = await context.new_page()
        await page.set_content(html_content)
        await page.wait_for_load_state('networkidle')
        await page.set_viewport_size({'width': 1200, 'height': 1080})
        await page.screenshot(path=f"{module_path}/out/{user_id}.png", full_page=True)
        await browser.close()