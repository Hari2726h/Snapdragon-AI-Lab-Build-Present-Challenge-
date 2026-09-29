const $ = (id) => document.getElementById(id);
const message = $("message");
const examples = {
  kyc: "Dear customer, your SBI KYC expires today. To avoid account suspension, verify immediately at sbi-kyc-secure.xyz and share the OTP sent to your mobile. Pay Rs 10 processing fee to verify@upi.",
  arrest: "Police Cyber Cell: You are under digital arrest for an illegal parcel. Stay on the call, do not tell anyone, and transfer ₹25,000 immediately to avoid legal action.",
  job: "Congratulations! You are selected for a remote job. Deposit INR 2,999 to hrdesk@upi today to unlock your laptop and offer letter.",
  boss: "Finance head here. I cannot take calls. Purchase five vouchers and send the numbers before the client meeting.",
  safe: "Official security notice: never share your OTP, PIN, CVV, or password. Report suspicious requests through the bank's official app."
};
let lastResult = null;
let analysisCount = 0;

message.addEventListener("input", () => $("counter").textContent = `${message.value.length.toLocaleString()} / 5,000`);
document.querySelectorAll("[data-example]").forEach(button => button.addEventListener("click", () => {
  message.value = examples[button.dataset.example];
  message.dispatchEvent(new Event("input"));
  message.focus();
}));
$("privacyButton").addEventListener("click", () => $("privacyDialog").showModal());
$("closeDialog").addEventListener("click", () => $("privacyDialog").close());
document.addEventListener("keydown", event => {
  if ((event.ctrlKey || event.metaKey) && event.key === "Enter") analyze();
});
$("analyzeButton").addEventListener("click", analyze);

async function analyze(){
  const text = message.value.trim();
  if(!text){message.focus();message.setAttribute("aria-invalid","true");return;}
  message.removeAttribute("aria-invalid");
  const button = $("analyzeButton");
  button.disabled = true; button.querySelector("span").textContent = "Scanning locally...";
  try{
    const response = await fetch("/api/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})});
    const result = await response.json();
    if(!response.ok) throw new Error(result.error || "Analysis failed");
    lastResult = result; analysisCount += 1; updatePrivacyCounter(); render(result);
  }catch(error){alert(error.message);}
  finally{button.disabled=false;button.querySelector("span").textContent="Analyze privately";}
}

function render(data){
  $("emptyState").classList.add("hidden"); $("result").classList.remove("hidden");
  $("score").textContent=data.score; $("riskGauge").style.setProperty("--score",data.score);
  const color=data.level==="high"?"var(--red)":data.level==="medium"?"var(--amber)":"var(--mint)";
  $("riskGauge").style.background=`conic-gradient(${color} ${data.score}%, #183028 0)`;
  $("riskLabel").textContent=`${data.level.toUpperCase()} RISK`; $("riskLabel").style.color=color;
  $("verdict").textContent=data.verdict; $("summary").textContent=data.summary;
  $("modelMeta").textContent=`${data.model.label.toUpperCase()} • ${(data.model.confidence*100).toFixed(1)}% confidence`;
  $("latency").textContent=`${data.meta.latency_ms} ms • local`;
  $("signals").replaceChildren(...(data.signals.length?data.signals.map(s=>{
    const row=document.createElement("div");row.className="signal-item";
    const dot=document.createElement("span");dot.className="dot";dot.style.background=color;
    const body=document.createElement("div");const title=document.createElement("strong");title.textContent=s.title;
    const detail=document.createElement("p");detail.textContent=s.detail;body.append(title,detail);
    const evidence=document.createElement("em");evidence.textContent=s.evidence;row.append(dot,body,evidence);return row;
  }):[Object.assign(document.createElement("p"),{textContent:"No strong indicators detected. Continue to verify unexpected requests."})]));
  $("primaryAction").textContent=data.actions[0];
  $("resultPanel").scrollIntoView({behavior:"smooth",block:"nearest"});
}

$("copyReport").addEventListener("click",async()=>{
  if(!lastResult)return;
  const report=[`Rakshak Edge: ${lastResult.verdict} (${lastResult.score}/100)`,lastResult.summary,"",...lastResult.signals.map(s=>`- ${s.title}: ${s.evidence}`),"",`Next: ${lastResult.actions[0]}`].join("\n");
  await navigator.clipboard.writeText(report); $("copyReport").textContent="Copied"; setTimeout(()=>$("copyReport").textContent="Copy safety report",1400);
});

$("downloadReport").addEventListener("click",()=>{
  if(!lastResult)return;
  downloadJson("rakshak-private-report.json", {
    generated_by:"Rakshak Edge", verdict:lastResult.verdict, score:lastResult.score,
    level:lastResult.level, evidence:lastResult.signals, recommended_actions:lastResult.actions,
    privacy:lastResult.meta.privacy, note:"The pasted source message is intentionally excluded."
  });
});

function updatePrivacyCounter(){ $("analysisCount").textContent=String(analysisCount); }

function downloadJson(filename,data){
  const blob=new Blob([JSON.stringify(data,null,2)],{type:"application/json"});
  const link=document.createElement("a");link.href=URL.createObjectURL(blob);link.download=filename;link.click();
  setTimeout(()=>URL.revokeObjectURL(link.href),500);
}

$("analyzeThread").addEventListener("click",analyzeConversation);

async function analyzeConversation(){
  const messages=[...document.querySelectorAll(".thread-message")].map((field,index)=>({role:index===0?"new contact":"sender",text:field.value.trim()}));
  if(messages.some(item=>!item.text)){document.querySelector(".thread-message:placeholder-shown")?.focus();return;}
  const button=$("analyzeThread");button.disabled=true;button.querySelector("span").textContent="Linking the attack chain...";
  try{
    const response=await fetch("/api/thread",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({messages})});
    const result=await response.json();if(!response.ok)throw new Error(result.error||"Conversation analysis failed");
    analysisCount+=1;updatePrivacyCounter();renderThread(result);
  }catch(error){alert(error.message);}
  finally{button.disabled=false;button.querySelector("span").textContent="Analyze conversation privately";}
}

function renderThread(data){
  $("threadEmpty").classList.add("hidden");$("threadResult").classList.remove("hidden");
  $("threadScore").textContent=data.score;$("threadLevel").textContent=`${data.level.toUpperCase()} RISK`;
  $("threadVerdict").textContent=data.verdict;$("threadAction").textContent=data.intervention[0];
  $("threadMeta").textContent=`Peak turn ${data.meta.peak_single_message_score} · progression +${data.meta.progression_bonus}`;
  $("threadTurns").replaceChildren(...data.turns.map(turn=>{
    const node=document.createElement("div");node.className=`turn turn-${turn.level}`;
    const top=document.createElement("div");const number=document.createElement("span");number.textContent=`0${turn.index}`;
    const score=document.createElement("strong");score.textContent=turn.score;top.append(number,score);
    const label=document.createElement("p");label.textContent=turn.top_signal;node.append(top,label);return node;
  }));
  $("attackChain").replaceChildren(...data.attack_chain.map((stage,index)=>{
    const node=document.createElement("div");node.className="chain-stage";
    const number=document.createElement("span");number.textContent=String(index+1).padStart(2,"0");
    const body=document.createElement("div");const title=document.createElement("strong");title.textContent=stage.title;
    const detail=document.createElement("p");detail.textContent=`Message ${stage.first_seen_at}: ${stage.detail}`;body.append(title,detail);node.append(number,body);return node;
  }));
  $("threadResult").scrollIntoView({behavior:"smooth",block:"nearest"});
}

const demo = new URLSearchParams(location.search).get("demo");
if (demo && examples[demo]) {
  document.body.classList.add("analysis-view");
  message.value = examples[demo];
  message.dispatchEvent(new Event("input"));
  analyze();
}
