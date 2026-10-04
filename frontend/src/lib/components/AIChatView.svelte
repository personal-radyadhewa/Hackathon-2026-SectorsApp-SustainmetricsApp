<script>
  import {
    Sparkles,
    Send,
    ArrowUp,
    SlidersHorizontal,
    Trash2,
    ShieldCheck,
    Building2,
    CheckCircle2,
    AlertCircle,
  } from '@lucide/svelte';

  let {
    activeTicker = 'PGEO',
    companyName = '',
  } = $props();

  let messages = $state([
    {
      role: 'assistant',
      content: `Hello! I'm your **Sustainability AI Assistant**.

I can answer questions regarding official disclosures, green capital expenditures, and OJK Green Taxonomy (TKBI 2024) compliance. What would you like to explore?`,
    },
  ]);

  let inputQuery = $state('');
  let isStreaming = $state(false);
  let provider = $state('gemini');
  let model = $state('gemini-2.5-flash');
  let apiKey = $state('');
  let showSettings = $state(false);

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

  function handleQuickPrompt(text) {
    inputQuery = text;
    handleSend();
  }

  function handleResetChat() {
    messages = [
      {
        role: 'assistant',
        content: `Chat cleared. Ask me anything about **${activeTicker}** or their environmental compliance.`,
      },
    ];
  }
</script>

<div class="max-w-4xl mx-auto h-[calc(100vh-8.5rem)] flex flex-col justify-between">
  <!-- Top Bar: Context & Quick Actions -->
  <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-xs flex items-center justify-between shrink-0 mb-4">
    <div class="flex items-center space-x-3">
      <div class="w-9 h-9 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
        <Sparkles size={18} />
      </div>
      <div>
        <h2 class="text-sm font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-2">
          <span>Ask AI about {activeTicker}</span>
          <span class="text-xs px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-mono font-medium">IDX:{activeTicker}</span>
        </h2>
        <p class="text-xs text-slate-500 dark:text-slate-400">
          Interactive assistant connected to audited financials & OJK TKBI 2024 criteria.
        </p>
      </div>
    </div>

    <div class="flex items-center space-x-1.5">
      <button
        type="button"
        onclick={() => (showSettings = !showSettings)}
        class="p-2 rounded-lg text-slate-500 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        title="AI Settings"
      >
        <SlidersHorizontal size={15} />
      </button>

      <button
        type="button"
        onclick={handleResetChat}
        class="p-2 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        title="Clear conversation"
      >
        <Trash2 size={15} />
      </button>
    </div>
  </div>

  <!-- Settings Panel (Collapsible) -->
  {#if showSettings}
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-xs mb-4 text-xs space-y-3">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div>
          <label for="provider-select" class="font-medium text-slate-700 dark:text-slate-300 block mb-1">Model Provider</label>
          <select
            id="provider-select"
            bind:value={provider}
            class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-900 dark:text-slate-100"
          >
            <option value="gemini">Google Gemini</option>
            <option value="openai">OpenAI</option>
            <option value="ollama">Ollama (Local)</option>
          </select>
        </div>

        <div>
          <label for="apikey-input" class="font-medium text-slate-700 dark:text-slate-300 block mb-1">API Key (Optional / Offline Default)</label>
          <input
            id="apikey-input"
            type="password"
            bind:value={apiKey}
            placeholder="System default key will be used if blank"
            class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs font-mono"
          />
        </div>
      </div>
    </div>
  {/if}

  <!-- Messages Scroll Area -->
  <div class="flex-1 overflow-y-auto space-y-4 pr-1 py-1">
    {#each messages as msg}
      <div class="flex flex-col {msg.role === 'user' ? 'items-end' : 'items-start'}">
        <span class="text-[10px] text-slate-400 dark:text-slate-500 mb-1 px-1 font-medium">
          {msg.role === 'user' ? 'You' : `AI Assistant (${activeTicker})`}
        </span>
        <div
          class="max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed whitespace-pre-wrap {msg.role === 'user'
            ? 'bg-slate-900 dark:bg-emerald-600 text-white rounded-tr-xs shadow-xs font-normal'
            : 'bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-200 rounded-tl-xs shadow-xs'}"
        >
          {msg.content}
        </div>
      </div>
    {/each}

    {#if isStreaming}
      <div class="flex items-center space-x-2 text-xs text-emerald-600 dark:text-emerald-400 animate-pulse py-2 px-2">
        <Sparkles size={14} />
        <span>Analyzing {activeTicker} disclosure reports & financial cash flows...</span>
      </div>
    {/if}
  </div>

  <!-- Prompt Suggestions & Input Box (Fixed at bottom of chat) -->
  <div class="mt-4 pt-2 shrink-0 space-y-2.5">
    <!-- Quick Question Chips -->
    <div class="flex gap-2 overflow-x-auto pb-1 text-xs">
      <button
        type="button"
        onclick={() => handleQuickPrompt(`What are the key greenwashing risks or disclosure gaps for ${activeTicker}?`)}
        class="whitespace-nowrap px-3 py-1.5 rounded-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors shadow-2xs"
      >
        🔍 Greenwashing risk check
      </button>
      <button
        type="button"
        onclick={() => handleQuickPrompt(`Break down ${activeTicker}'s capital expenditure into green vs conventional spending.`)}
        class="whitespace-nowrap px-3 py-1.5 rounded-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors shadow-2xs"
      >
        💰 Green spending vs Capex
      </button>
      <button
        type="button"
        onclick={() => handleQuickPrompt(`Is ${activeTicker} compliant with OJK TKBI Versi 3 technical criteria?`)}
        class="whitespace-nowrap px-3 py-1.5 rounded-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors shadow-2xs"
      >
        📋 TKBI compliance summary
      </button>
    </div>

    <!-- Main Input Bar -->
    <form
      onsubmit={(e) => { e.preventDefault(); handleSend(); }}
      class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-2 pl-4 shadow-sm flex items-center gap-2"
    >
      <input
        type="text"
        bind:value={inputQuery}
        placeholder={`Ask anything about ${activeTicker}...`}
        class="flex-1 bg-transparent text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none"
      />
      <button
        type="submit"
        disabled={isStreaming || !inputQuery.trim()}
        class="w-8 h-8 rounded-xl bg-slate-900 dark:bg-emerald-500 hover:bg-slate-800 dark:hover:bg-emerald-400 text-white dark:text-slate-950 flex items-center justify-center transition-all disabled:opacity-40 shadow-xs shrink-0"
      >
        <ArrowUp size={16} />
      </button>
    </form>
  </div>
</div>
