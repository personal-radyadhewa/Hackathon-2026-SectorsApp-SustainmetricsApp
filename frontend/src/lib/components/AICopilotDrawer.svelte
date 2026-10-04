<script>
  import { Bot, Send, X, Sparkles, CheckCircle2, ChevronDown, Key, SlidersHorizontal } from '@lucide/svelte';

  let {
    isOpen = false,
    onClose,
    activeTicker = 'PGEO',
  } = $props();

  let messages = $state([
    {
      role: 'assistant',
      content: `Hello! I'm your **Sustainability Copilot**. I analyze official Indonesian company disclosures, sustainability reports, and verified financial filings.

Ask me anything about company environmental compliance, green investments, or taxonomy criteria.`,
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
    class="fixed inset-0 bg-black/40 backdrop-blur-2xs z-40 transition-opacity"
    onclick={onClose}
    onkeydown={(e) => e.key === 'Escape' && onClose()}
    role="button"
    tabindex="0"
  ></div>

  <!-- Slide-out Drawer (Hermes Agent Style) -->
  <aside class="fixed top-0 right-0 w-[440px] max-w-full h-screen bg-white dark:bg-slate-900 border-l border-slate-200 dark:border-slate-800 shadow-2xl z-50 flex flex-col justify-between animate-in slide-in-from-right duration-200">
    <!-- Header -->
    <div class="px-5 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-950/40">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-800/60 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
          <Bot size={18} />
        </div>
        <div>
          <h3 class="text-sm font-semibold text-slate-900 dark:text-slate-100 flex items-center gap-1.5">
            Sustainability Copilot
          </h3>
          <p class="text-[11px] text-slate-500 dark:text-slate-400">Context: <span class="font-semibold text-slate-700 dark:text-slate-300 font-mono">{activeTicker}</span></p>
        </div>
      </div>

      <div class="flex items-center space-x-1">
        <button
          type="button"
          onclick={() => (showKeySettings = !showKeySettings)}
          class="p-2 rounded-md text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          title="AI Settings"
        >
          <SlidersHorizontal size={15} />
        </button>
        <button
          type="button"
          onclick={onClose}
          class="p-2 rounded-md text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
          title="Close"
        >
          <X size={16} />
        </button>
      </div>
    </div>

    <!-- Provider Configuration Panel (Collapsible) -->
    {#if showKeySettings}
      <div class="p-4 bg-slate-50 dark:bg-slate-950 border-b border-slate-200 dark:border-slate-800 text-xs space-y-3">
        <div>
          <label for="copilot-provider" class="text-[11px] font-medium text-slate-600 dark:text-slate-400 block mb-1">AI Provider</label>
          <select
            id="copilot-provider"
            bind:value={provider}
            class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-md px-3 py-1.5 text-slate-800 dark:text-slate-200 text-xs focus:outline-none"
          >
            <option value="gemini">Google Gemini</option>
            <option value="openai">OpenAI</option>
            <option value="ollama">Ollama (Local)</option>
          </select>
        </div>

        <div>
          <label for="copilot-apikey" class="text-[11px] font-medium text-slate-600 dark:text-slate-400 block mb-1">API Key (Optional / Uses System Default)</label>
          <input
            id="copilot-apikey"
            type="password"
            bind:value={apiKey}
            placeholder="AIzaSy... / sk-..."
            class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-md px-3 py-1.5 text-xs text-slate-800 dark:text-slate-200 focus:outline-none font-mono"
          />
        </div>
      </div>
    {/if}

    <!-- Chat Messages Scroll Area -->
    <div class="flex-1 overflow-y-auto p-5 space-y-4">
      {#each messages as msg}
        <div class="flex flex-col {msg.role === 'user' ? 'items-end' : 'items-start'}">
          <span class="text-[10px] text-slate-400 dark:text-slate-500 mb-1 px-1 font-medium">
            {msg.role === 'user' ? 'You' : 'Sustainability Copilot'}
          </span>
          <div
            class="max-w-[92%] rounded-2xl p-3.5 text-xs leading-relaxed whitespace-pre-wrap {msg.role === 'user'
              ? 'bg-slate-900 dark:bg-emerald-600 text-white rounded-tr-xs shadow-xs font-normal'
              : 'bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 text-slate-800 dark:text-slate-200 rounded-tl-xs shadow-2xs'}"
          >
            {msg.content}
          </div>
        </div>
      {/each}

      {#if isStreaming}
        <div class="flex items-center space-x-2 text-xs text-emerald-600 dark:text-emerald-400 animate-pulse py-1 px-2">
          <Sparkles size={14} />
          <span>Analyzing sustainability reports & financials...</span>
        </div>
      {/if}
    </div>

    <!-- Quick Prompts Chips -->
    <div class="px-4 py-2.5 border-t border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/30 flex gap-2 overflow-x-auto">
      <button
        type="button"
        onclick={() => sendQuickPrompt(`Are there any greenwashing risks for ${activeTicker}?`)}
        class="whitespace-nowrap px-3 py-1.5 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-xs text-slate-700 dark:text-slate-300 rounded-full border border-slate-200 dark:border-slate-700 transition-colors shadow-2xs"
      >
        🔍 Greenwashing risk check
      </button>
      <button
        type="button"
        onclick={() => sendQuickPrompt(`How much does ${activeTicker} spend on green projects vs conventional business?`)}
        class="whitespace-nowrap px-3 py-1.5 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-xs text-slate-700 dark:text-slate-300 rounded-full border border-slate-200 dark:border-slate-700 transition-colors shadow-2xs"
      >
        💰 Green spending breakdown
      </button>
      <button
        type="button"
        onclick={() => sendQuickPrompt(`What are the key environmental criteria for ${activeTicker}?`)}
        class="whitespace-nowrap px-3 py-1.5 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-xs text-slate-700 dark:text-slate-300 rounded-full border border-slate-200 dark:border-slate-700 transition-colors shadow-2xs"
      >
        📋 Requirements summary
      </button>
    </div>

    <!-- Input Footer -->
    <form onsubmit={(e) => { e.preventDefault(); handleSend(); }} class="p-3.5 border-t border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 flex gap-2">
      <input
        type="text"
        bind:value={inputQuery}
        placeholder={`Ask a question about ${activeTicker}...`}
        class="flex-1 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl px-3.5 py-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-emerald-500 shadow-2xs"
      />
      <button
        type="submit"
        disabled={isStreaming || !inputQuery.trim()}
        class="p-2.5 rounded-xl bg-slate-900 dark:bg-emerald-500 hover:bg-slate-800 dark:hover:bg-emerald-400 text-white dark:text-slate-950 font-medium transition-colors shadow-xs disabled:opacity-40"
      >
        <Send size={15} />
      </button>
    </form>
  </aside>
{/if}
