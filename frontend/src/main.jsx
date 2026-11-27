import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { Activity, AudioLines, Brain, CalendarDays, ChevronDown, Circle, Folder, Grid2X2, History, Mail, MessageSquare, Mic, Network, Plug, Plus, Settings2, User, Workflow, Globe, FileText, Youtube, Instagram, Linkedin, Facebook, Send, Paperclip, PanelLeft, Search, Bell, Monitor, Zap, CircleHelp, X, Trash2 } from 'lucide-react';
import './styles.css';

const API_BASE = import.meta.env.VITE_JARVIS_API_URL || 'http://127.0.0.1:8000';
const nav = [
 {label:'NETWORK',icon:Network},{label:'DASHBOARD',icon:Grid2X2},{label:'TALK',icon:AudioLines},{label:'WORKFLOWS',icon:Workflow},
 {label:'FILES',icon:Folder},{label:'CONNECTIONS',icon:Plug},{label:'ASSISTANT',icon:Settings2},{label:'ACCOUNT',icon:User}
];
const nodes = [
 {name:'Reddit',icon:MessageSquare,x:43,y:8},{name:'Gmail',icon:Mail,x:61,y:8,active:true,badge:3},
 {name:'Voice',icon:AudioLines,x:51,y:23,active:true,badge:7},{name:'Google Calendar',icon:CalendarDays,x:77,y:19,active:true},
 {name:'Facebook',icon:Facebook,x:29,y:19},{name:'Web',icon:Globe,x:34,y:39,active:true},{name:'Chat',icon:MessageSquare,x:68,y:39,active:true},
 {name:'Google Drive',icon:Folder,x:86,y:35,active:true},{name:'Twitter',icon:CircleHelp,x:18,y:35},
 {name:'LinkedIn',icon:Linkedin,x:18,y:56},{name:'Files',icon:Folder,x:40,y:64,active:true,badge:2},
 {name:'Memory',icon:Brain,x:61,y:64,active:true,badge:7},{name:'Google Docs',icon:FileText,x:86,y:55,active:true,badge:4},
 {name:'Instagram',icon:Instagram,x:27,y:75},{name:'YouTube',icon:Youtube,x:43,y:84},
 {name:'Notion',icon:Network,x:61,y:84,active:true},{name:'Google Sheets',icon:Grid2X2,x:77,y:75,active:true,badge:6}
];
function NeuralCore(){return <div className="core-wrap"><div className="core-halo halo-one"/><div className="core-halo halo-two"/><div className="core-ring ring-a"/><div className="core-ring ring-b"/><div className="core"><Brain size={72} strokeWidth={1.1}/><span>J-A-R-V-I-S</span></div><div className="core-pulse"/></div>}
function NetworkCanvas(){
 const [selected,setSelected]=useState('Voice');
 return <div className="network-canvas"><div className="grid-glow"/>
 <svg className="connections" viewBox="0 0 100 100" preserveAspectRatio="none">{nodes.map((n,i)=><g key={n.name}><line x1="51" y1="48" x2={n.x} y2={n.y} className={n.active?'link link-active':'link'}/>{n.active&&<circle r=".35" className="link-particle"><animateMotion dur={(4+i%4)+'s'} repeatCount="indefinite" path={'M 51 48 L '+n.x+' '+n.y}/></circle>}</g>)}</svg>
 <NeuralCore/>{nodes.map(({name,icon:Icon,x,y,active,badge})=><button key={name} className={'network-node '+(active?'active':'idle')+(selected===name?' selected':'')} style={{left:x+'%',top:y+'%'}} onClick={()=>setSelected(name)} aria-label={'Select '+name}><span className="node-icon"><Icon size={17}/></span>{badge&&<span className="node-badge">{badge}</span>}<span className="node-label">{name}</span></button>)}
 <div className="network-top-left"><div className="eyebrow">NEURAL NETWORK</div><span>Network visualization · prototype</span></div><div className="network-top-right"><span className="live-pill"><i/> UI ACTIVE</span><button className="activity-btn"><Activity size={13}/> Activity</button></div><div className="selected-node-note">Selected: {selected}</div><div className="network-bottom-hint">Tap to explore</div></div>;
}
function App(){
 const [message,setMessage]=useState(''),[listening,setListening]=useState(false),[activeNav,setActiveNav]=useState('NETWORK');
 const [conversationId,setConversationId]=useState(null),[messages,setMessages]=useState([]),[sending,setSending]=useState(false),[apiState,setApiState]=useState('checking'),[showMessages,setShowMessages]=useState(false);
 const [conversations,setConversations]=useState([]),[loadingHistory,setLoadingHistory]=useState(true);
 const refreshConversations=async()=>{try{const r=await fetch(API_BASE+'/api/conversations');if(!r.ok)throw new Error();const data=await r.json();setConversations(Array.isArray(data)?data:(data.conversations||[]));setApiState('connected')}catch{setApiState('offline')}finally{setLoadingHistory(false)}};
 useEffect(()=>{fetch(API_BASE+'/api/health').then(r=>r.ok?setApiState('connected'):setApiState('offline')).catch(()=>setApiState('offline'));refreshConversations()},[]);
 const openConversation=async id=>{try{const r=await fetch(API_BASE+'/api/conversations/'+id+'/history');if(!r.ok)throw new Error('Unable to load conversation');const data=await r.json();const history=Array.isArray(data)?data:(data.messages||[]);setConversationId(id);setMessages(history);setShowMessages(true);setMessage('')}catch(e){setApiState('offline')}};
 const deleteConversation=async(id,e)=>{e.stopPropagation();try{const r=await fetch(API_BASE+'/api/conversations/'+id,{method:'DELETE'});if(!r.ok)throw new Error();setConversations(prev=>prev.filter(c=>c.id!==id));if(conversationId===id)newConversation()}catch{setApiState('offline')}};
 const sendMessage=async()=>{
  const text=message.trim();if(!text||sending)return;
  setMessage('');setShowMessages(true);setSending(true);
  setMessages(prev=>[...prev,{role:'user',content:text}]);
  try{
   const response=await fetch(API_BASE+'/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text,conversation_id:conversationId})});
   if(!response.ok)throw new Error('API request failed ('+response.status+')');
   const data=await response.json();setConversationId(data.conversation_id);setApiState('connected');
   setMessages(prev=>[...prev,{role:'assistant',content:data.reply,mode:data.mode}]);
   await refreshConversations();
  }catch(err){setApiState('offline');setMessages(prev=>[...prev,{role:'assistant',content:'Unable to reach the J-A-R-V-I-S backend. Start the backend locally and retry. Error: '+err.message,error:true}]);}
  finally{setSending(false)}
 };
 const newConversation=()=>{setConversationId(null);setMessages([]);setShowMessages(false);setMessage('')};
 return <div className="app-shell"><aside className="sidebar"><div className="brand-row"><div className="brand-mark"><Brain size={18}/></div><span className="brand-name">J-A-R-V-I-S</span><button className="sidebar-collapse"><PanelLeft size={15}/></button></div><button className="new-chat" onClick={newConversation}><Plus size={15}/> NEW CONVERSATION</button><nav className="navigation">{nav.map(({label,icon:Icon})=><button key={label} className={'nav-item '+(activeNav===label?'active':'')} onClick={()=>setActiveNav(label)}><Icon size={15}/><span>{label}</span></button>)}</nav><div className="history"><div className="history-heading"><History size={13}/> HISTORY <span className="history-count">{conversations.length}</span></div>{loadingHistory?<div className="history-empty">Loading saved chats…</div>:conversations.length?conversations.map(c=><div key={c.id} className={'history-row '+(conversationId===c.id?'selected':'')}><button className="history-item" onClick={()=>openConversation(c.id)}><span>{c.title||'Conversation'}</span><small>{c.updated_at?new Date(c.updated_at).toLocaleDateString():''}</small></button><button className="history-delete" title="Delete conversation" onClick={e=>deleteConversation(c.id,e)}><Trash2 size={12}/></button></div>):<div className="history-empty">No saved conversations</div>}</div><div className="sidebar-footer"><div className="profile-avatar">D</div><div className="profile-info"><strong>Local User</strong><small>Personal workspace</small></div><ChevronDown size={14}/></div></aside>
 <main className="main-panel"><header className="page-header"><div className="header-title">{activeNav==='NETWORK'?'Network':activeNav.charAt(0)+activeNav.slice(1).toLowerCase()}</div><div className="header-actions"><button className="icon-button"><Search size={16}/></button><button className="icon-button"><Bell size={16}/></button><button className="icon-button"><Settings2 size={16}/></button></div></header><section className="workspace"><NetworkCanvas/><div className="conversation-bar">{showMessages&&messages.length>0&&<div className="chat-messages">{messages.map((m,i)=><div key={i} className={'chat-message '+m.role+(m.error?' error':'')}><b>{m.role==='user'?'You':'J-A-R-V-I-S'}</b><p>{m.content}</p></div>)}{sending&&<div className="chat-message assistant"><b>J-A-R-V-I-S</b><p>Processing…</p></div>}<button className="close-messages" onClick={()=>setShowMessages(false)} aria-label="Hide conversation"><X size={14}/></button></div>}<div className="greeting">{messages.length?'Conversation active':'Hi there! How can I assist you today?'}</div><div className={'voice-state '+(listening?'is-listening':'')}><span>{listening?'Listening':'Voice idle'}</span><AudioLines size={15}/><button className="mic-toggle" onClick={()=>setListening(!listening)} aria-label="Toggle microphone"><Mic size={15}/></button></div><form className="message-input" onSubmit={e=>{e.preventDefault();sendMessage()}}><button type="button" className="attach-button" title="Attachment UI (not implemented)"><Paperclip size={16}/></button><input value={message} onChange={e=>setMessage(e.target.value)} placeholder="Type to Jarvis while you talk..."/><button className="send-button" disabled={!message.trim()||sending} type="submit"><Send size={16}/></button></form></div></section><footer className="status-footer"><span><Circle size={7} fill="currentColor"/> UI</span><span><Zap size={12}/> API {apiState}</span><span><Monitor size={12}/> Desktop-ready layout</span><span className="footer-right">J-A-R-V-I-S · 0.3.0</span></footer></main></div>;
}
createRoot(document.getElementById('root')).render(<App/>);
