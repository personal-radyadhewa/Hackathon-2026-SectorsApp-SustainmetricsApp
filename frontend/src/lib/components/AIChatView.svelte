<script>
  import {
    Sparkles,
    Paperclip,
    Search,
    ChevronDown,
    Mic,
    ArrowUp,
    Plus,
    SlidersHorizontal,
    Trash2,
  } from '@lucide/svelte';

  let {
    activeTicker = 'PGEO',
    companyName = '',
  } = $props();

  let messages = $state([]);
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

    // Append empty assistant placeholder to populate via SSE
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

  function handleNewChat() {
    messages = [];
    inputQuery = '';
  }
</script>

<div class="flex-1 flex flex-col h-[calc(100vh-6.5rem)] overflow-hidden">
  <!-- Top Bar: Title & Action Pills -->
  <div class="px-6 py-3 flex items-center justify-between shrink-0 border-b border-slate-200/80 dark:border-slate-800 bg-white/70 dark:bg-[#0F172A]/70 backdrop-blur-xs">
    <div class="flex items-center space-x-2.5">
      <h1 class="text-base font-headline font-bold text-slate-900 dark:text-slate-100 tracking-tight">Ask AI Assistant</h1>
      <span class="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-[#162032] text-slate-700 dark:text-slate-300 font-mono border border-slate-200 dark:border-slate-800">
        IDX:{activeTicker}
      </span>
    </div>

    <div class="flex items-center space-x-2">
      <button
        type="button"
        onclick={() => (showSettings = !showSettings)}
        class="flex items-center space-x-1.5 px-3 py-1.5 rounded-full border border-slate-200 dark:border-slate-700 text-xs font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-[#162032] transition-colors cursor-pointer shadow-2xs"
        title="Settings"
      >
        <SlidersHorizontal size={13} />
        <span>Settings</span>
      </button>

      <button
        type="button"
        onclick={handleNewChat}
        class="flex items-center space-x-1 px-3.5 py-1.5 rounded-full bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] text-xs font-semibold transition-colors cursor-pointer shadow-xs"
      >
        <Plus size={14} />
        <span>New chat</span>
      </button>
    </div>
  </div>

  <!-- Settings Panel (Collapsible) -->
  {#if showSettings}
    <div class="mx-6 mt-3 p-4 bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm text-xs space-y-3">
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div>
          <label for="chat-provider" class="font-medium text-slate-700 dark:text-slate-300 block mb-1">Model Provider</label>
          <select
            id="chat-provider"
            bind:value={provider}
            class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-900 dark:text-slate-100 font-medium"
          >
            <option value="gemini">Google Gemini (Default)</option>
            <option value="openai">OpenAI</option>
            <option value="ollama">Ollama (Local)</option>
          </select>
        </div>

        <div>
          <label for="chat-apikey" class="font-medium text-slate-700 dark:text-slate-300 block mb-1">API Key (Optional / Uses System Default)</label>
          <input
            id="chat-apikey"
            type="password"
            bind:value={apiKey}
            placeholder="AIzaSy... / sk-..."
            class="w-full bg-slate-50 dark:bg-[#162032] border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs font-mono"
          />
        </div>
      </div>
    </div>
  {/if}

  <!-- Content Area -->
  {#if messages.length === 0}
    <!-- Hero State: Centered Title & Preserved Chat Box -->
    <div class="flex-1 flex flex-col items-center justify-center p-6 max-w-2xl mx-auto w-full -mt-6">
      <!-- Clean Hero Headline -->
      <h2 class="text-2xl md:text-3xl font-headline font-light text-slate-800 dark:text-slate-200 tracking-tight text-center mb-6">
        Hello, what's on <strong class="font-bold text-slate-950 dark:text-white">your mind?</strong>
      </h2>

      <!-- The Chat Box -->
      <div class="w-full bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-3xl shadow-sm hover:shadow-md transition-shadow p-4">
        <!-- Input Top Row with Sparkle Icon -->
        <div class="flex items-start space-x-2.5 mb-4 px-1">
          <Sparkles size={16} class="text-[#047857] dark:text-[#34D399] shrink-0 mt-0.5" />
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
            class="w-full bg-transparent text-xs font-body text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none resize-none leading-relaxed"
          ></textarea>
        </div>

        <!-- Chat Box Bottom Action Bar -->
        <div class="flex items-center justify-between pt-2.5 border-t border-slate-100 dark:border-slate-800 px-1">
          <div class="flex items-center space-x-3 text-xs text-slate-500 dark:text-slate-400">
            <button
              type="button"
              onclick={() => handleQuickPrompt(`Check environmental criteria citations for ${activeTicker}`)}
              class="flex items-center space-x-1.5 hover:text-slate-900 dark:hover:text-slate-200 transition-colors cursor-pointer"
            >
              <Paperclip size={14} />
              <span>Attach</span>
            </button>

            <button
              type="button"
              onclick={() => handleQuickPrompt(`Verify OJK TKBI compliance status for ${activeTicker}`)}
              class="flex items-center space-x-1.5 hover:text-slate-900 dark:hover:text-slate-200 transition-colors cursor-pointer"
            >
              <Search size={14} />
              <span>Search</span>
            </button>

            <div class="flex items-center space-x-1 text-slate-700 dark:text-slate-300">
              <span>Company: {activeTicker}</span>
              <ChevronDown size={12} />
            </div>
          </div>

          <div class="flex items-center space-x-2">
            <button
              type="button"
              class="p-1.5 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors"
              title="Voice query"
            >
              <Mic size={16} />
            </button>

            <button
              type="button"
              onclick={handleSend}
              disabled={isStreaming || !inputQuery.trim()}
              class="w-8 h-8 rounded-full bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] flex items-center justify-center transition-all disabled:opacity-40 cursor-pointer shadow-xs"
            >
              <ArrowUp size={16} />
            </button>
          </div>
        </div>
      </div>

      <!-- Quick Question Suggestions below chat box -->
      <div class="flex flex-wrap justify-center gap-2 mt-5 text-xs">
        <button
          type="button"
          onclick={() => handleQuickPrompt(`What are the primary greenwashing risks for ${activeTicker}?`)}
          class="px-3.5 py-1.5 rounded-full bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-50 dark:hover:bg-[#162032] transition-colors shadow-2xs cursor-pointer"
        >
          🔍 Greenwashing risks
        </button>
        <button
          type="button"
          onclick={() => handleQuickPrompt(`Compare ${activeTicker}'s operating cash flow vs green capital expenditure.`)}
          class="px-3.5 py-1.5 rounded-full bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-50 dark:hover:bg-[#162032] transition-colors shadow-2xs cursor-pointer"
        >
          💰 Capex vs Disclosures
        </button>
        <button
          type="button"
          onclick={() => handleQuickPrompt(`Show OJK TKBI Versi 3 criteria alignment for ${activeTicker}.`)}
          class="px-3.5 py-1.5 rounded-full bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-slate-100 hover:bg-slate-50 dark:hover:bg-[#162032] transition-colors shadow-2xs cursor-pointer"
        >
          📋 TKBI Taxonomy criteria
        </button>
      </div>
    </div>
  {:else}
    <!-- Active Conversation Mode -->
    <div class="flex-1 flex flex-col justify-between overflow-hidden px-6 py-4 max-w-3xl mx-auto w-full">
      <div class="flex-1 overflow-y-auto space-y-4 pr-1">
        {#each messages as msg}
          <div class="flex flex-col {msg.role === 'user' ? 'items-end' : 'items-start'}">
            <span class="text-[10px] text-slate-400 dark:text-slate-500 mb-1 px-1 font-medium font-mono">
              {msg.role === 'user' ? 'You' : `AI Assistant (${activeTicker})`}
            </span>
            <div
              class="max-w-[85%] rounded-2xl p-4 text-xs leading-relaxed whitespace-pre-wrap {msg.role === 'user'
                ? 'bg-[#047857] text-white rounded-tr-xs shadow-xs font-normal'
                : 'bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 text-slate-800 dark:text-slate-200 rounded-tl-xs shadow-xs'}"
            >
              {msg.content}
            </div>
          </div>
        {/each}

        {#if isStreaming}
          <div class="flex items-center space-x-2 text-xs text-[#047857] dark:text-[#34D399] animate-pulse py-2 px-2 font-mono">
            <Sparkles size={14} />
            <span>Analyzing {activeTicker} disclosure reports &amp; financial cash flows...</span>
          </div>
        {/if}
      </div>

      <!-- Bottom Chat Box in Conversation Mode -->
      <div class="mt-3 pt-2 shrink-0">
        <div class="w-full bg-white dark:bg-[#0F172A] border border-slate-200/80 dark:border-slate-800 rounded-2xl shadow-sm p-3">
          <div class="flex items-center space-x-2">
            <input
              type="text"
              bind:value={inputQuery}
              onkeydown={(e) => e.key === 'Enter' && handleSend()}
              placeholder={`Ask a follow-up about ${activeTicker}...`}
              class="flex-1 bg-transparent text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none px-2"
            />
            <button
              type="button"
              onclick={handleSend}
              disabled={isStreaming || !inputQuery.trim()}
              class="w-7 h-7 rounded-full bg-[#047857] hover:bg-[#065F46] dark:bg-[#34D399] dark:hover:bg-[#10B981] text-white dark:text-[#064E3B] flex items-center justify-center transition-all disabled:opacity-40 cursor-pointer shadow-xs"
            >
              <ArrowUp size={14} />
            </button>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>
