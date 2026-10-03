import os, json, time, logging, urllib.parse, urllib.request, urllib.error, threading
from http.server import BaseHTTPRequestHandler, HTTPServer
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log=logging.getLogger("al-ezz-bot")
BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN", "").strip(); API_KEY=os.getenv("TRENDAWE_API_KEY", "").strip(); API_URL=os.getenv("TRENDAWE_API_URL", "https://trendawe.com/api/v2").strip()
if not BOT_TOKEN: raise RuntimeError("Missing Railway Variable: TELEGRAM_BOT_TOKEN")
if not API_KEY: raise RuntimeError("Missing Railway Variable: TRENDAWE_API_KEY")
TG=f"https://api.telegram.org/bot{BOT_TOKEN}"
WA_ACCESS_TOKEN=os.getenv("WHATSAPP_ACCESS_TOKEN", "").strip()
WA_PHONE_NUMBER_ID=os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip()
WA_VERIFY_TOKEN=os.getenv("WHATSAPP_VERIFY_TOKEN", "").strip()
WA_GRAPH_URL=f"https://graph.facebook.com/v20.0/{WA_PHONE_NUMBER_ID}/messages" if WA_PHONE_NUMBER_ID else ""
WA_SESSIONS={}
SERVICES=[
  {
    "id": "5953",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "متابعين فيسبوك للطلبات التي تزيد عن 40,000 | البداية: 0–10 دقائق | السرعة: 100,000 في اليوم 🚀 | الجودة: ملفات تعريف مخفية | إعادة التعبئة: 60 يومًا ♻️ | نسبة السقوط: 0% | الرابط: صفحة أو ملف تعريف فيسبوك",
    "price": "0.1338"
  },
  {
    "id": "2673",
    "platform": "Facebook",
    "category": "Followers / Members",
    "description": "متابعين فيسبوك — حسابات عالمية حقيقية 🌟 | البداية: فورية 🚀 | السرعة: 100,000 في اليوم | إعادة التعبئة: 30 يومًا ♻️ | الرابط: صفحة أو ملف تعريف فيسبوك",
    "price": "غير محدد"
  },
  {
    "id": "4675",
    "platform": "Facebook",
    "category": "Likes / Reactions",
    "description": "لايكات فيسبوك | البداية: 0–1 دقيقة 🚀 | السرعة: 50,000 في اليوم | إعادة التعبئة: لا توجد إعادة تعبئة ⚠️ | مثال الرابط: نص أو صور — رابط كامل",
    "price": "غير محدد"
  }
]; SESSIONS={}
PLATFORMS=sorted(set(s['platform'] for s in SERVICES)); CATEGORIES={p:sorted(set(s['category'] for s in SERVICES if s['platform']==p)) for p in PLATFORMS}

def post(url,data,timeout=60):
 req=urllib.request.Request(url,data=urllib.parse.urlencode(data).encode(),method='POST'); req.add_header('Content-Type','application/x-www-form-urlencoded')
 with urllib.request.urlopen(req,timeout=timeout) as r:return json.loads(r.read().decode())
def tg(method,data): return post(f"{TG}/{method}",data)
def send(cid,text,markup=None):
 d={'chat_id':str(cid),'text':text}; 
 if markup:d['reply_markup']=json.dumps({'inline_keyboard':markup},ensure_ascii=False)
 tg('sendMessage',d)
def edit(cid,mid,text,markup=None):
 d={'chat_id':str(cid),'message_id':str(mid),'text':text}
 if markup:d['reply_markup']=json.dumps({'inline_keyboard':markup},ensure_ascii=False)
 tg('editMessageText',d)
def answer(qid):
 try:tg('answerCallbackQuery',{'callback_query_id':qid})
 except:pass
def button(text,data):return {'text':text,'callback_data':data}
def platform_menu():
 return [[button(p,f'p:{i}') for i,p in enumerate(PLATFORMS[j:j+2])] for j in range(0,len(PLATFORMS),2)]
def category_menu(pi):
 cs=CATEGORIES[PLATFORMS[pi]]; return [[button(c,f'c:{pi}:{i}')] for i,c in enumerate(cs)]+[[button('⬅️ رجوع','home')]]
def service_menu(pi,ci,page=0):
 p=PLATFORMS[pi]; c=CATEGORIES[p][ci]; items=[s for s in SERVICES if s['platform']==p and s['category']==c]; size=8; part=items[page*size:(page+1)*size]
 rows=[[button(f"{s['id']} | {s['price'] + '$' if s['price'] != 'غير محدد' else 'السعر غير محدد'}",f"s:{pi}:{ci}:{s['id']}") ] for s in part]
 nav=[]
 if page>0:nav.append(button('⬅️ السابق',f'pg:{pi}:{ci}:{page-1}'))
 if (page+1)*size<len(items):nav.append(button('التالي ➡️',f'pg:{pi}:{ci}:{page+1}'))
 if nav:rows.append(nav)
 rows.append([button('⬅️ الأقسام','pback'),button('🏠 الرئيسية','home')]); return rows,len(items),part

def home(cid,mid=None):
 text='أهلًا بك في @AlEzzMediaBot\n\nاختر المنصة المطلوبة:'; m=platform_menu()
 if mid:edit(cid,mid,text,m)
 else:send(cid,text,m)
def handle_callback(q):
 answer(q.get('id')); d=q.get('data',''); msg=q.get('message',{}); cid=msg.get('chat',{}).get('id'); mid=msg.get('message_id')
 if cid is None:return
 if d=='home':home(cid,mid);return
 if d=='pback':home(cid,mid);return
 if d.startswith('p:'):
  pi=int(d.split(':')[1]); edit(cid,mid,f"منصة {PLATFORMS[pi]}\nاختر القسم:",category_menu(pi));return
 if d.startswith('c:'):
  _,pi,ci=d.split(':'); pi=int(pi);ci=int(ci); m,n,part=service_menu(pi,ci); edit(cid,mid,f"{PLATFORMS[pi]} — {CATEGORIES[PLATFORMS[pi]][ci]}\nاختر الخدمة (السعر لكل 1000):",m);return
 if d.startswith('pg:'):
  _,pi,ci,page=d.split(':');m,n,part=service_menu(int(pi),int(ci),int(page));edit(cid,mid,f"اختر الخدمة ({n} خدمة):",m);return
 if d.startswith('s:'):
  _,pi,ci,sid=d.split(':'); s=next(x for x in SERVICES if x['id']==sid); SESSIONS[cid]={'step':'link','service':sid,'description':s['description']}; edit(cid,mid,f"الخدمة المختارة:\n{s['description']}\n\nأرسل الرابط أو اسم المستخدم.",[ [button('❌ إلغاء','cancel')] ]);return
 if d=='cancel':SESSIONS.pop(cid,None);edit(cid,mid,'تم إلغاء الطلب.');return

def handle_message(m):
 cid=m.get('chat',{}).get('id'); text=(m.get('text') or '').strip()
 if cid is None:return
 if text in ('/start','/help'):home(cid);return
 if text=='/cancel':SESSIONS.pop(cid,None);send(cid,'تم إلغاء الطلب.');return
 s=SESSIONS.get(cid)
 if not s:send(cid,'اضغط /start للبدء.');return
 if s['step']=='link':
  if not text:send(cid,'أرسل الرابط أو اسم المستخدم.');return
  s['link']=text;s['step']='quantity';send(cid,'أرسل الكمية بالأرقام.');return
 if s['step']=='quantity':
  try:q=int(text);assert 1<=q<=1000000
  except:send(cid,'أرسل كمية صحيحة بين 1 و 1,000,000.');return
  send(cid,'جارٍ إرسال الطلب...')
  try:
   r=post(API_URL,{'key':API_KEY,'action':'add','service':s['service'],'link':s['link'],'quantity':str(q)})
   send(cid,f"تم الطلب بنجاح ✅\nرقم الطلب: {r['order']}" if r.get('order') else 'لم يتم إنشاء الطلب: '+str(r.get('error',r)))
  except Exception:log.exception('order failed');send(cid,'تعذر الاتصال بمنصة الطلبات. تحقق من مفتاح ترنداوي.')
  finally:SESSIONS.pop(cid,None)

def json_post(url, payload, headers=None, timeout=60):
 req=urllib.request.Request(url, data=json.dumps(payload, ensure_ascii=False).encode(), method='POST')
 req.add_header('Content-Type','application/json')
 for k,v in (headers or {}).items(): req.add_header(k,v)
 with urllib.request.urlopen(req, timeout=timeout) as r: return json.loads(r.read().decode())

def wa_send(to, text):
 if not WA_ACCESS_TOKEN or not WA_GRAPH_URL: return
 json_post(WA_GRAPH_URL, {'messaging_product':'whatsapp','to':str(to),'type':'text','text':{'preview_url':False,'body':text}}, {'Authorization':f'Bearer {WA_ACCESS_TOKEN}'})

def wa_services_text():
 return ('اختر الخدمة بإرسال رقمها فقط:\n\n'
         '5953 — متابعين فيسبوك للطلبات فوق 40,000\n'
         '2673 — متابعين فيسبوك بحسابات عالمية حقيقية\n'
         '4675 — لايكات فيسبوك\n\n'
         'أرسل /cancel للإلغاء.')

def handle_whatsapp_message(sender, text):
 text=(text or '').strip()
 state=WA_SESSIONS.get(sender)
 if text.lower() in ('/start','ابدأ','اهلا','أهلا','مرحبا','مرحباً') or not state:
  WA_SESSIONS[sender]={'step':'service'}
  wa_send(sender, 'أهلًا بك في AlEzz Media لخدمات فيسبوك.\n\n'+wa_services_text())
  return
 if text.lower() in ('/cancel','إلغاء','الغاء'):
  WA_SESSIONS.pop(sender,None); wa_send(sender,'تم إلغاء الطلب. أرسل /start للبدء من جديد.'); return
 if state['step']=='service':
  service=next((x for x in SERVICES if x['id']==text),None)
  if not service: wa_send(sender,'رقم الخدمة غير صحيح.\n\n'+wa_services_text()); return
  state.update({'step':'link','service':service['id']})
  wa_send(sender, f"الخدمة المختارة:\n{service['description']}\n\nأرسل رابط الصفحة أو الملف الشخصي.")
  return
 if state['step']=='link':
  state.update({'step':'quantity','link':text})
  wa_send(sender,'أرسل الكمية بالأرقام (مثال: 40000).'); return
 if state['step']=='quantity':
  try: quantity=int(text); assert 1<=quantity<=1000000
  except: wa_send(sender,'الكمية غير صحيحة. أرسل رقمًا بين 1 و 1,000,000.'); return
  wa_send(sender,'جارٍ إرسال الطلب...')
  try:
   r=post(API_URL,{'key':API_KEY,'action':'add','service':state['service'],'link':state['link'],'quantity':str(quantity)})
   if r.get('order'): wa_send(sender,f"تم إنشاء الطلب بنجاح ✅\nرقم الطلب: {r['order']}")
   else: wa_send(sender,'لم يتم إنشاء الطلب: '+str(r.get('error',r)))
  except Exception:
   log.exception('whatsapp order failed'); wa_send(sender,'تعذر الاتصال بمنصة الطلبات. تحقق من إعدادات ترنداوي.')
  finally: WA_SESSIONS.pop(sender,None)

def whatsapp_payload(payload):
 try:
  for entry in payload.get('entry',[]):
   for change in entry.get('changes',[]):
    value=change.get('value',{})
    for msg in value.get('messages',[]):
     if msg.get('type')=='text': handle_whatsapp_message(msg.get('from'), msg.get('text',{}).get('body',''))
 except Exception: log.exception('whatsapp webhook failed')

class WhatsAppHandler(BaseHTTPRequestHandler):
 def log_message(self, fmt, *args): log.info('WhatsApp webhook: '+fmt, *args)
 def do_GET(self):
  q=urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
  if q.get('hub.mode',[''])[0]=='subscribe' and q.get('hub.verify_token',[''])[0]==WA_VERIFY_TOKEN and WA_VERIFY_TOKEN:
   body=q.get('hub.challenge',[''])[0].encode(); self.send_response(200); self.end_headers(); self.wfile.write(body); return
  self.send_response(403); self.end_headers()
 def do_POST(self):
  try:
   n=int(self.headers.get('Content-Length','0')); payload=json.loads(self.rfile.read(n).decode())
   whatsapp_payload(payload); self.send_response(200); self.end_headers(); self.wfile.write(b'OK')
  except Exception:
   log.exception('invalid WhatsApp webhook payload'); self.send_response(400); self.end_headers()

def start_whatsapp_webhook():
 if not (WA_ACCESS_TOKEN and WA_PHONE_NUMBER_ID and WA_VERIFY_TOKEN):
  log.info('WhatsApp webhook disabled: set WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_VERIFY_TOKEN')
  return
 port=int(os.getenv('PORT','8080')); HTTPServer(('0.0.0.0',port),WhatsAppHandler).serve_forever()

def main():
 threading.Thread(target=start_whatsapp_webhook, daemon=True).start()
 off=0;log.info('started with %s services',len(SERVICES))
 while True:
  try:
   r=post(f"{TG}/getUpdates",{'offset':str(off),'timeout':'50','allowed_updates':json.dumps(['message','callback_query'])},65)
   for u in r.get('result',[]):
    off=u['update_id']+1
    if u.get('callback_query'):handle_callback(u['callback_query'])
    elif u.get('message'):
     try:handle_message(u['message'])
     except Exception:log.exception('handler failed')
  except Exception:log.exception('poll failed');time.sleep(5)
if __name__=='__main__':main()
