<script>
  import {
    Paperclip,
    Search,
    ChevronDown,
    Mic,
    ArrowUp,
    Sparkles,
    FolderPlus,
    Plus,
    Bot,
    Send,
  } from '@lucide/svelte';

  let {
    activeTicker = 'PGEO',
    onSelectTicker,
  } = $props();

  let messages = $state([]);
  let inputQuery = $state('');
  let isStreaming = $state(false);
  let provider = $state('gemini');
  let model = $state('gemini-2.5-flash');
  let apiKey = $state('');
  let selectedScope = $state('Current Company');

  async function handleSend() {
    if (!inputQuery.trim() || isStreaming) return;
    const userMsg = inputQuery.trim();
    inputQuery = '';

    messages = [...messages, { role: 'user', content: userMsg }];
    isStreaming = true;

    // Append assistant placeholder
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
      messages[assistantIndex].content = `\n\n❌ Connection error: ${err.message}`;
    } finally {
      isStreaming = false;
    }
  }

  function handleNewChat() {
    messages = [];
    inputQuery = '';
  }

  function handleQuickPrompt(text) {
    inputQuery = text;
    handleSend();
  }
</script>

<div class="flex-1 flex flex-col h-full overflow-hidden">
  <!-- View Top Sub-Header (exact reference) -->
  <div class="px-8 pt-6 pb-2 flex items-center justify-between shrink-0">
    <h1 class="text-xl font-semibold text-slate-900 dark:text-slate-100 tracking-tight">Ask AI</h1>

    <div class="flex items-center space-x-2.5">
      <button
        type="button"
        class="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-full border border-slate-200 dark:border-slate-800 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors shadow-2xs"
      >
        <Search size={13} class="text-slate-400" />
        <span>Search thread</span>
      </button>

      <button
        type="button"
        class="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-full border border-slate-200 dark:border-slate-800 text-xs font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors shadow-2xs"
      >
        <FolderPlus size={13} class="text-slate-400" />
        <span>Create folder</span>
      </button>

      <button
        type="button"
        onclick={handleNewChat}
        class="flex items-center space-x-1 px-4 py-1.5 rounded-full bg-slate-950 dark:bg-emerald-500 hover:bg-slate-800 dark:hover:bg-emerald-400 text-white dark:text-slate-950 text-xs font-medium transition-all shadow-xs"
      >
        <Plus size={14} />
        <span>New chat</span>
      </button>
    </div>
  </div>

  <!-- Content Body -->
  {#if messages.length === 0}
    <!-- Hero State (exact reference) -->
    <div class="flex-1 flex flex-col items-center justify-center p-6 -mt-8 max-w-3xl mx-auto w-full">
      <!-- Minimalist Smart Assistant Device Graphic -->
      <div class="relative w-44 h-56 mb-8 flex items-center justify-center select-none">
        <!-- Soft Ambient Glow -->
        <div class="absolute inset-0 bg-gradient-to-t from-slate-200/50 dark:from-slate-800/40 to-transparent rounded-full blur-2xl transform scale-90"></div>

        <!-- 3D Mesh Speaker Device Visual -->
        <div class="relative w-36 h-48 rounded-[44px] bg-gradient-to-b from-white via-slate-50 to-slate-100 dark:from-slate-800 dark:via-slate-850 dark:to-slate-900 shadow-xl border border-slate-200/80 dark:border-slate-700/60 overflow-hidden flex flex-col items-center justify-center">
          <!-- Mesh Texture -->
          <div class="absolute inset-0 opacity-15 dark:opacity-25" style="background-image: radial-gradient(#64748b 1px, transparent 1px); background-size: 5px 5px;"></div>
          
          <!-- Top Cap Contour -->
          <div class="absolute top-0 inset-x-0 h-6 bg-gradient-to-b from-slate-100 dark:from-slate-700 to-transparent rounded-t-[44px]"></div>

          <!-- Subtle Digital Clock Display on Mesh (from reference) -->
          <div class="relative z-10 text-center font-mono tracking-wider text-slate-300 dark:text-slate-500 text-2xl font-light leading-tight select-none">
            <div>08</div>
            <div>30</div>
          </div>

          <!-- Bottom Soft Shadow -->
          <div class="absolute bottom-0 inset-x-0 h-4 bg-gradient-to-t from-slate-200/60 dark:from-slate-900 to-transparent"></div>
        </div>
      </div>

      <!-- Hero Headline -->
      <h2 class="text-3xl font-light text-slate-800 dark:text-slate-200 tracking-tight text-center mb-8">
        Hello, what's on <strong class="font-bold text-slate-950 dark:text-white">your mind?</strong>
      </h2>

      <!-- Floating Prompt Box (exact reference styling) -->
      <div class="w-full bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 rounded-3xl shadow-sm hover:shadow-md transition-shadow p-4 relative">
        <!-- Top Prompt Input -->
        <div class="flex items-start space-x-2.5 mb-6 px-1">
          <Sparkles size={16} class="text-blue-500 shrink-0 mt-0.5" />
          <textarea
            bind:value={inputQuery}
            onkeydown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder={`Ask me anything about ${activeTicker} or Indonesia Green Taxonomy (TKBI)...`}
            rows="2"
            class="w-full bg-transparent text-sm text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none resize-none"
          ></textarea>
        </div>

        <!-- Bottom Action Bar (Attach, Search, Scope Dropdown, Mic, Arrow Send) -->
        <div class="flex items-center justify-between pt-2 border-t border-slate-100 dark:border-slate-800/80 px-1">
          <div class="flex items-center space-x-3 text-xs text-slate-500 dark:text-slate-400">
            <button
              type="button"
              onclick={() => handleQuickPrompt(`Analyze report citations for ${activeTicker}`)}
              class="flex items-center space-x-1.5 hover:text-slate-900 dark:hover:text-slate-200 transition-colors"
            >
              <Paperclip size={14} />
              <span>Attach</span>
            </button>

            <button
              type="button"
              onclick={() => handleQuickPrompt(`Search OJK TKBI compliance for ${activeTicker}`)}
              class="flex items-center space-x-1.5 hover:text-slate-900 dark:hover:text-slate-200 transition-colors"
            >
              <Search size={14} />
              <span>Search</span>
            </button>

            <div class="flex items-center space-x-1 hover:text-slate-900 dark:hover:text-slate-200 cursor-pointer">
              <span>Company: {activeTicker}</span>
              <ChevronDown size={12} />
            </div>
          </div>

          <div class="flex items-center space-x-2">
            <button
              type="button"
              class="p-2 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors"
              title="Voice input"
            >
              <Mic size={16} />
            </button>

            <button
              type="button"
              onclick={handleSend}
              disabled={isStreaming || !inputQuery.trim()}
              class="w-8 h-8 rounded-full bg-slate-950 dark:bg-emerald-500 hover:bg-slate-800 dark:hover:bg-emerald-400 text-white dark:text-slate-950 flex items-center justify-center transition-all disabled:opacity-40 shadow-xs"
            >
              <ArrowUp size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  {:else}
    <!-- Active Chat Conversation View -->
    <div class="flex-1 flex flex-col justify-between overflow-hidden px-8 py-4 max-w-4xl mx-auto w-full">
      <div class="flex-1 overflow-y-auto space-y-4 pr-2">
        {#each messages as msg}
          <div class="flex flex-col {msg.role === 'user' ? 'items-end' : 'items-start'}">
            <span class="text-[10px] text-slate-400 dark:text-slate-500 mb-1 px-1 font-medium">
              {msg.role === 'user' ? 'You' : 'AI Assistant'}
            </span>
            <div
              class="max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed whitespace-pre-wrap {msg.role === 'user'
                ? 'bg-slate-950 dark:bg-emerald-600 text-white rounded-tr-xs shadow-xs'
                : 'bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700/80 text-slate-800 dark:text-slate-200 rounded-tl-xs shadow-xs'}"
            >
              {msg.content}
            </div>
          </div>
        {/each}

        {#if isStreaming}
          <div class="flex items-center space-x-2 text-xs text-blue-600 dark:text-emerald-400 animate-pulse py-2 px-2">
            <Sparkles size={14} />
            <span>AI is analyzing company filings and taxonomy criteria...</span>
          </div>
        {/if}
      </div>

      <!-- Bottom Chat Bar in Conversation Mode -->
      <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800">
        <div class="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm p-3">
          <div class="flex items-center space-x-2">
            <input
              type="text"
              bind:value={inputQuery}
              onkeydown={(e) => e.key === 'Enter' && handleSend()}
              placeholder={`Ask a follow-up question about ${activeTicker}...`}
              class="flex-1 bg-transparent text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none px-2"
            />
            <button
              type="button"
              onclick={handleSend}
              disabled={isStreaming || !inputQuery.trim()}
              class="w-7 h-7 rounded-full bg-slate-950 dark:bg-emerald-500 hover:bg-slate-800 dark:hover:bg-emerald-400 text-white dark:text-slate-950 flex items-center justify-center transition-all disabled:opacity-40 shadow-xs"
            >
              <ArrowUp size={14} />
            </button>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>
