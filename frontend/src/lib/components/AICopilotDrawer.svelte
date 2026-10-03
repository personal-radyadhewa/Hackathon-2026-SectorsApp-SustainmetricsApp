<script>
  import { Bot, Send, X, Sparkles, CheckCircle2, ChevronDown, Key } from '@lucide/svelte';

  let {
    isOpen = false,
    onClose,
    activeTicker = 'PGEO',
  } = $props();

  let messages = $state([
    {
      role: 'assistant',
      content: `Hello! I'm your **SustainMetric AI Copilot**. I have real-time access to the FastMCP server, OJK TKBI 2024 technical taxonomy rules, and Sectors fundamental financials. Ask me anything about IDX tickers or technical criteria.`,
    },
  ]);

  let inputQuery = $state('');
  let isStreaming = $state(false);
  let provider = $state('gemini');
  let model = $state('gemini-2.5-flash');
  let apiKey = $state('');
  let showKeySettings = $state(false);

  async function handleSend() {
    if (!inputQuery.trim() || isStreaming) return;
    const userMsg = inputQuery.trim();
    inputQuery = '';

    messages = [...messages, { role: 'user', content: userMsg }];
    isStreaming = true;

    // Append empty assistant message to populate via SSE
    messages = [...messages, { role: 'assistant', content: '' }];
    const assistantIndex = messages.length - 1;

    try {
      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: messages.slice(0, assistantIndex),
          provider,
          model,
          api_key: apiKey,
        }),
      });

      if (!response.ok) {
        messages[assistantIndex].content = `⚠️ Server error: ${response.statusText}`;
        isStreaming = false;
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.includes('event: delta')) {
            const dataMatch = line.match(/data: (.+)/);
            if (dataMatch) {
              try {
                const parsed = JSON.parse(dataMatch[1]);
                if (parsed.content) {
                  messages[assistantIndex].content += parsed.content;
                }
              } catch (e) {}
            }
          } else if (line.includes('event: done')) {
            isStreaming = false;
          }
        }
      }
    } catch (err) {
      messages[assistantIndex].content += `\n\n❌ Connection error: ${err.message}`;
    } finally {
      isStreaming = false;
    }
  }

  function sendQuickPrompt(promptText) {
    inputQuery = promptText;
    handleSend();
  }
</script>

{#if isOpen}
  <!-- Backdrop -->
  <div
    class="fixed inset-0 bg-black/60 backdrop-blur-xs z-40 transition-opacity"
    onclick={onClose}
    onkeydown={(e) => e.key === 'Escape' && onClose()}
    role="button"
    tabindex="0"
  ></div>

  <!-- Slide-out Drawer -->
  <aside class="fixed top-0 right-0 w-[420px] max-w-full h-screen bg-white dark:bg-[#0E1527] border-l border-slate-200 dark:border-[#1E293B] shadow-2xl z-50 flex flex-col justify-between animate-in slide-in-from-right duration-200">
    <!-- Header -->
    <div class="px-4 py-3.5 border-b border-slate-200 dark:border-[#1E293B] flex items-center justify-between bg-[#0F162B]">
      <div class="flex items-center space-x-2">
        <div class="w-7 h-7 rounded-md bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-400">
          <Bot size={16} />
        </div>
        <div>
          <h3 class="text-xs font-bold text-slate-900 dark:text-slate-100 flex items-center gap-1.5">
            SustainMetric Copilot
            <span class="text-[9px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-mono">FastMCP</span>
          </h3>
          <p class="text-[10px] text-slate-500 dark:text-slate-400">Active context: <span class="font-mono text-emerald-400 font-semibold">{activeTicker}</span></p>
        </div>
      </div>

      <div class="flex items-center space-x-1">
        <button
          type="button"
          onclick={() => (showKeySettings = !showKeySettings)}
          class="p-1.5 rounded text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:text-slate-200 hover:bg-slate-200 dark:bg-[#1E293B] transition-colors"
          title="LLM Provider Settings"
        >
          <Key size={14} />
        </button>
        <button
          type="button"
          onclick={onClose}
          class="p-1.5 rounded text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:text-slate-200 hover:bg-slate-200 dark:bg-[#1E293B] transition-colors"
        >
          <X size={15} />
        </button>
      </div>
    </div>

    <!-- Provider Configuration Panel (Collapsible) -->
    {#if showKeySettings}
      <div class="p-3 bg-white dark:bg-[#0E1527] border-b border-slate-200 dark:border-[#1E293B] text-xs space-y-2">
        <div class="flex items-center justify-between">
          <label for="copilot-provider" class="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400">Provider</label>
          <select
            id="copilot-provider"
            bind:value={provider}
            class="bg-slate-50 dark:bg-[#090E1A] border border-slate-200 dark:border-[#1E293B] rounded px-2 py-1 text-slate-800 dark:text-slate-200 text-xs focus:outline-none"
          >
            <option value="gemini">Google Gemini</option>
            <option value="openai">OpenAI</option>
            <option value="ollama">Ollama (Local)</option>
          </select>
        </div>

        <div>
          <label for="copilot-apikey" class="text-[10px] uppercase font-semibold text-slate-500 dark:text-slate-400 block mb-1">API Key (Optional / Offline Default)</label>
          <input
            id="copilot-apikey"
            type="password"
            bind:value={apiKey}
            placeholder="AIzaSy... / sk-..."
            class="w-full bg-slate-50 dark:bg-[#090E1A] border border-slate-200 dark:border-[#1E293B] rounded px-2 py-1 text-xs text-slate-800 dark:text-slate-200 focus:outline-none focus:border-emerald-500/50 font-mono"
          />
        </div>
      </div>
    {/if}

    <!-- Chat Messages Scroll Area -->
    <div class="flex-1 overflow-y-auto p-4 space-y-3.5">
      {#each messages as msg}
        <div class="flex flex-col {msg.role === 'user' ? 'items-end' : 'items-start'}">
          <span class="text-[10px] text-slate-400 dark:text-slate-500 mb-1 font-mono uppercase">
            {msg.role === 'user' ? 'Auditor' : 'Copilot AI'}
          </span>
          <div
            class="max-w-[90%] rounded-lg p-3 text-xs leading-relaxed whitespace-pre-wrap {msg.role === 'user'
              ? 'bg-emerald-600 text-slate-50 font-medium'
              : 'bg-white dark:bg-[#0E1527] border border-slate-200 dark:border-[#1E293B] text-slate-800 dark:text-slate-200 shadow-sm'}"
          >
            {msg.content}
          </div>
        </div>
      {/each}

      {#if isStreaming}
        <div class="flex items-center space-x-2 text-xs text-emerald-400 animate-pulse py-1">
          <Sparkles size={13} />
          <span>Executing FastMCP tool reasoning...</span>
        </div>
      {/if}
    </div>

    <!-- Quick Prompts Chips -->
    <div class="px-3 py-2 border-t border-slate-200 dark:border-[#1E293B] bg-white dark:bg-[#0E1527]/40 flex gap-1.5 overflow-x-auto">
      <button
        type="button"
        onclick={() => sendQuickPrompt(`Audit greenwashing flags for ${activeTicker}`)}
        class="whitespace-nowrap px-2 py-1 bg-slate-100 dark:bg-[#151E33] hover:bg-slate-200 dark:bg-[#1E293B] text-[11px] text-slate-700 dark:text-slate-300 rounded border border-slate-200 dark:border-[#1E293B] transition-colors"
      >
        🔍 Greenwashing flags
      </button>
      <button
        type="button"
        onclick={() => sendQuickPrompt(`Compare ${activeTicker} Capex allocation vs disclosures`)}
        class="whitespace-nowrap px-2 py-1 bg-slate-100 dark:bg-[#151E33] hover:bg-slate-200 dark:bg-[#1E293B] text-[11px] text-slate-700 dark:text-slate-300 rounded border border-slate-200 dark:border-[#1E293B] transition-colors"
      >
        💰 Capex Reality Check
      </button>
      <button
        type="button"
        onclick={() => sendQuickPrompt(`Show OJK TKBI TSC threshold for ${activeTicker}`)}
        class="whitespace-nowrap px-2 py-1 bg-slate-100 dark:bg-[#151E33] hover:bg-slate-200 dark:bg-[#1E293B] text-[11px] text-slate-700 dark:text-slate-300 rounded border border-slate-200 dark:border-[#1E293B] transition-colors"
      >
        📋 TKBI Criteria
      </button>
    </div>

    <!-- Input Footer -->
    <form onsubmit={(e) => { e.preventDefault(); handleSend(); }} class="p-3 border-t border-slate-200 dark:border-[#1E293B] bg-[#0F162B] flex gap-2">
      <input
        type="text"
        bind:value={inputQuery}
        placeholder={`Ask Copilot about ${activeTicker} or TKBI criteria...`}
        class="flex-1 bg-white dark:bg-[#0E1527] border border-slate-200 dark:border-[#1E293B] rounded-lg px-3 py-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500/50"
      />
      <button
        type="submit"
        disabled={isStreaming || !inputQuery.trim()}
        class="p-2 rounded-lg bg-slate-900 dark:bg-emerald-500 hover:bg-slate-800 dark:hover:bg-emerald-400 text-white dark:text-slate-950 font-bold transition-colors disabled:opacity-40"
      >
        <Send size={15} />
      </button>
    </form>
  </aside>
{/if}
