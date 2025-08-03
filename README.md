<span class="">
   <h1>VAP2D - Visual Analysis Platform for 2D Data</h1>
   <p class="first:mt-1.5">VAP2D is a visual analysis and data processing platform for two-dimensional data. This software allows users to easily analyze, visualize, and extract meaningful insights from 2D data using both traditional methods and deep learning-based object detection techniques.</p>
   <h2>✨ Features</h2>
   <ul class="list-disc">
      <li class="ml-4"><strong class="">📊 Data Visualization</strong>: Analyze your 2D data with graphs and visual tools</li>
      <li class="ml-4"><strong class="">⚙️ Data Processing</strong>: Perform various operations on your data</li>
      <li class="ml-4"><strong class="">🤖 Deep Learning Integration</strong>: Advanced object detection using Detectron2</li>
      <li class="ml-4"><strong class="">🖥️ User-Friendly Interface</strong>: Simple and intuitive PySide6-based GUI</li>
      <li class="ml-4"><strong class="">🌐 Cross-Platform Support</strong>: Runs on Windows, Linux, and macOS</li>
      <li class="ml-4"><strong class="">🐳 Docker Support</strong>: Easy deployment with multi-platform Docker images</li>
   </ul>
   <h2>🚀 Quick Start with Docker (Recommended)</h2>
   <p class="first:mt-1.5">The easiest way to run VAP2D is using Docker:</p>
   <pre><div data-gramm="false" class=" relative bg-neutral-50 dark:bg-neutral-800 mb-2 rounded-[0.625rem]"><div class=" sticky top-0 bg-neutral-100 dark:bg-neutral-700 mt-[7px] rounded-t-[0.625rem] px-[14px] font-normal py-[6px] flex items-center SimTextWrite_codeHeader___xVjD justify-between">bash<div class="flex items-center gap-3"><div class=" flex items-center gap-[4px] text-[12px] text-darkcolor/[0.5] !cursor-pointer hover:text-darkcolor/[0.7] p-[2px] pt-[4px] rounded "><svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="copy" class="svg-inline--fa fa-copy " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"></path></svg><span class="w-[40px]">Copy</span></div></div></div><div class="px-[15px] py-[10px] rounded-b-[4px]" style="font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace;"><span class="hljs-comment"># Pull and run the latest version  </span>
docker pull sametkaya/vap2d:v2.1  
docker run sametkaya/vap2d:v2.1  
</div></div></pre>
   <h3>🖼️ Docker with GUI Support</h3>
   <h4>🐧 Linux</h4>
   <pre><div data-gramm="false" class=" relative bg-neutral-50 dark:bg-neutral-800 mb-2 rounded-[0.625rem]"><div class=" sticky top-0 bg-neutral-100 dark:bg-neutral-700 mt-[7px] rounded-t-[0.625rem] px-[14px] font-normal py-[6px] flex items-center SimTextWrite_codeHeader___xVjD justify-between">bash<div class="flex items-center gap-3"><div class=" flex items-center gap-[4px] text-[12px] text-darkcolor/[0.5] !cursor-pointer hover:text-darkcolor/[0.7] p-[2px] pt-[4px] rounded "><svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="copy" class="svg-inline--fa fa-copy " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"></path></svg><span class="w-[40px]">Copy</span></div></div></div><div class="px-[15px] py-[10px] rounded-b-[4px]" style="font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace;">docker run -e DISPLAY=<span class="hljs-variable">$DISPLAY</span> -v /tmp/.X11-unix:/tmp/.X11-unix sametkaya/vap2d:v2.1  
</div></div></pre>
   <h4>🪟 Windows</h4>
   <ol class="list-decimal">
      <li class="ml-4">Install <a href="https://sourceforge.net/projects/vcxsrv/" target="_blank" rel="noopener noreferrer" class="break-word">VcXsrv</a> or <a href="https://sourceforge.net/projects/xming/" target="_blank" rel="noopener noreferrer" class="break-word">Xming</a></li>
      <li class="ml-4">Start the X server with "Disable access control" enabled</li>
      <li class="ml-4">Run the container:</li>
   </ol>
   <pre><div data-gramm="false" class=" relative bg-neutral-50 dark:bg-neutral-800 mb-2 rounded-[0.625rem]"><div class=" sticky top-0 bg-neutral-100 dark:bg-neutral-700 mt-[7px] rounded-t-[0.625rem] px-[14px] font-normal py-[6px] flex items-center SimTextWrite_codeHeader___xVjD justify-between">bash<div class="flex items-center gap-3"><div class=" flex items-center gap-[4px] text-[12px] text-darkcolor/[0.5] !cursor-pointer hover:text-darkcolor/[0.7] p-[2px] pt-[4px] rounded "><svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="copy" class="svg-inline--fa fa-copy " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"></path></svg><span class="w-[40px]">Copy</span></div></div></div><div class="px-[15px] py-[10px] rounded-b-[4px]" style="font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace;">docker run -e DISPLAY=host.docker.internal:0 sametkaya/vap2d:v2.1  
</div></div></pre>
   <h4>🍎 macOS</h4>
   <ol class="list-decimal">
      <li class="ml-4">Install <a href="https://www.xquartz.org/" target="_blank" rel="noopener noreferrer" class="break-word">XQuartz</a></li>
      <li class="ml-4">Start XQuartz and enable "Allow connections from network clients"</li>
      <li class="ml-4">Run the container:</li>
   </ol>
   <pre><div data-gramm="false" class=" relative bg-neutral-50 dark:bg-neutral-800 mb-2 rounded-[0.625rem]"><div class=" sticky top-0 bg-neutral-100 dark:bg-neutral-700 mt-[7px] rounded-t-[0.625rem] px-[14px] font-normal py-[6px] flex items-center SimTextWrite_codeHeader___xVjD justify-between">bash<div class="flex items-center gap-3"><div class=" flex items-center gap-[4px] text-[12px] text-darkcolor/[0.5] !cursor-pointer hover:text-darkcolor/[0.7] p-[2px] pt-[4px] rounded "><svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="copy" class="svg-inline--fa fa-copy " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"></path></svg><span class="w-[40px]">Copy</span></div></div></div><div class="px-[15px] py-[10px] rounded-b-[4px]" style="font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace;">docker run -e DISPLAY=host.docker.internal:0 sametkaya/vap2d:v2.1  
</div></div></pre>
   <h2>💻 Local Installation</h2>
   <h3>📋 Requirements</h3>
   <ul class="list-disc">
      <li class="ml-4">Python 3.10 or higher</li>
      <li class="ml-4">Required Python libraries (listed in <code data-gramm="false">requirements.txt</code>)</li>
   </ul>
   <h3>🔧 Installation Steps</h3>
   <ol class="list-decimal">
      <li class="ml-4">
         <p class="first:mt-1.5"><strong class="">Clone the repository:</strong></p>
         <pre><div data-gramm="false" class=" relative bg-neutral-50 dark:bg-neutral-800 mb-2 rounded-[0.625rem]"><div class=" sticky top-0 bg-neutral-100 dark:bg-neutral-700 mt-[7px] rounded-t-[0.625rem] px-[14px] font-normal py-[6px] flex items-center SimTextWrite_codeHeader___xVjD justify-between">bash<div class="flex items-center gap-3"><div class=" flex items-center gap-[4px] text-[12px] text-darkcolor/[0.5] !cursor-pointer hover:text-darkcolor/[0.7] p-[2px] pt-[4px] rounded "><svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="copy" class="svg-inline--fa fa-copy " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"></path></svg><span class="w-[40px]">Copy</span></div></div></div><div class="px-[15px] py-[10px] rounded-b-[4px]" style="font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace;">git <span class="hljs-built_in">clone</span> https://github.com/sametkaya/vap2d.git  
<span class="hljs-built_in">cd</span> vap2d  
</div></div></pre>
      </li>
      <li class="ml-4">
         <p class="first:mt-1.5"><strong class="">Create a virtual environment (recommended):</strong></p>
         <pre><div data-gramm="false" class=" relative bg-neutral-50 dark:bg-neutral-800 mb-2 rounded-[0.625rem]"><div class=" sticky top-0 bg-neutral-100 dark:bg-neutral-700 mt-[7px] rounded-t-[0.625rem] px-[14px] font-normal py-[6px] flex items-center SimTextWrite_codeHeader___xVjD justify-between">bash<div class="flex items-center gap-3"><div class=" flex items-center gap-[4px] text-[12px] text-darkcolor/[0.5] !cursor-pointer hover:text-darkcolor/[0.7] p-[2px] pt-[4px] rounded "><svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="copy" class="svg-inline--fa fa-copy " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"></path></svg><span class="w-[40px]">Copy</span></div></div></div><div class="px-[15px] py-[10px] rounded-b-[4px]" style="font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace;">python -m venv venv  
<span class="hljs-comment"># On Windows:  </span>
venv\Scripts\activate  
<span class="hljs-comment"># On Linux/macOS:  </span>
<span class="hljs-built_in">source</span> venv/bin/activate  
</div></div></pre>
      </li>
      <li class="ml-4">
         <p class="first:mt-1.5"><strong class="">Install the required dependencies:</strong></p>
         <pre><div data-gramm="false" class=" relative bg-neutral-50 dark:bg-neutral-800 mb-2 rounded-[0.625rem]"><div class=" sticky top-0 bg-neutral-100 dark:bg-neutral-700 mt-[7px] rounded-t-[0.625rem] px-[14px] font-normal py-[6px] flex items-center SimTextWrite_codeHeader___xVjD justify-between">bash<div class="flex items-center gap-3"><div class=" flex items-center gap-[4px] text-[12px] text-darkcolor/[0.5] !cursor-pointer hover:text-darkcolor/[0.7] p-[2px] pt-[4px] rounded "><svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="copy" class="svg-inline--fa fa-copy " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"></path></svg><span class="w-[40px]">Copy</span></div></div></div><div class="px-[15px] py-[10px] rounded-b-[4px]" style="font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace;">pip install -r requirements.txt  
</div></div></pre>
      </li>
      <li class="ml-4">
         <p class="first:mt-1.5"><strong class="">Run the application:</strong></p>
         <pre><div data-gramm="false" class=" relative bg-neutral-50 dark:bg-neutral-800 mb-2 rounded-[0.625rem]"><div class=" sticky top-0 bg-neutral-100 dark:bg-neutral-700 mt-[7px] rounded-t-[0.625rem] px-[14px] font-normal py-[6px] flex items-center SimTextWrite_codeHeader___xVjD justify-between">bash<div class="flex items-center gap-3"><div class=" flex items-center gap-[4px] text-[12px] text-darkcolor/[0.5] !cursor-pointer hover:text-darkcolor/[0.7] p-[2px] pt-[4px] rounded "><svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="copy" class="svg-inline--fa fa-copy " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"></path></svg><span class="w-[40px]">Copy</span></div></div></div><div class="px-[15px] py-[10px] rounded-b-[4px]" style="font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace;">python main.py  
</div></div></pre>
      </li>
   </ol>
   <h2>📖 Usage</h2>
   <ol class="list-decimal">
      <li class="ml-4">After starting the application, you can load your data and use the analysis tools from the main menu</li>
      <li class="ml-4">Use the visualization options to display your data as graphs</li>
      <li class="ml-4">Process and analyze your data using the available tools</li>
      <li class="ml-4">Generate comprehensive reports with analysis results</li>
   </ol>
   <h2>📸 Screenshots</h2>
   <h4>Load raw image</h4>
   <img src="doc/screens/scrn1.png" alt="Screen 1" width="300">
   <h4>Denoising</h4>
   <img src="doc/screens/scrn2.png" alt="Screen 1" width="300">
   <h4>Segmentation</h4>
   <img src="doc/screens/scrn3.png" alt="Screen 1" width="300">
   <h4>Analyse</h4>
   <img src="doc/screens/scrn5.png" alt="Screen 1" width="300">
   <h4>Show only branch points</h4>
   <img src="doc/screens/scrn6.png" alt="Screen 1" width="300">
   <h4>Show only endpoints</h4>
   <img src="doc/screens/scrn7.png" alt="Screen 1" width="300">
   <h4>Show only vessel path with infos</h4>
   <img src="doc/screens/scrn8.png" alt="Screen 1" width="300">
   <h4>Zooming</h4>
   <img src="doc/screens/scrn9.png" alt="Screen 1" width="300">
   <h4>All Prepocesses</h4>
   <img src="doc/screens/scrn_preproces.png" alt="Screen 1" width="300">
   <h4>All view actions</h4>
   <img src="doc/screens/scrn_analyse.png" alt="Screen 1" width="300">
   <h4>Report Screen</h4>
   <img src="doc/screens/scrn_report.png" alt="Screen 1" width="300">
   <h2>🐳 Docker Information</h2>
   <ul class="list-disc">
      <li class="ml-4"><strong class="">🏠 Repository</strong>: <a href="https://hub.docker.com/r/sametkaya/vap2d" target="_blank" rel="noopener noreferrer" class="break-word">https://hub.docker.com/r/sametkaya/vap2d</a></li>
      <li class="ml-4"><strong class="">🏷️ Version</strong>: v2.1</li>
      <li class="ml-4"><strong class="">🌍 Supported Platforms</strong>: Linux (AMD64, ARM64), Windows (via Docker Desktop)</li>
      <li class="ml-4"><strong class="">🔗 Persistent Identifier</strong>: <code data-gramm="false">docker://sametkaya/vap2d:v2.1</code></li>
   </ul>
   <h2>💾 System Requirements</h2>
   <h3>📊 Minimum Requirements</h3>
   <ul class="list-disc">
      <li class="ml-4"><strong class="">OS</strong>: Windows 10/11, Ubuntu 18.04+, macOS 10.15+</li>
      <li class="ml-4"><strong class="">RAM</strong>: 8 GB</li>
      <li class="ml-4"><strong class="">Storage</strong>: 2 GB free space</li>
      <li class="ml-4"><strong class="">GPU</strong>: Optional (CUDA-compatible for enhanced performance)</li>
   </ul>
   <h3>🚀 Recommended Requirements</h3>
   <ul class="list-disc">
      <li class="ml-4"><strong class="">OS</strong>: Windows 11, Ubuntu 20.04+, macOS 12+</li>
      <li class="ml-4"><strong class="">RAM</strong>: 16 GB or more</li>
      <li class="ml-4"><strong class="">Storage</strong>: 5 GB free space</li>
      <li class="ml-4"><strong class="">GPU</strong>: NVIDIA GPU with CUDA support</li>
   </ul>
   <h2>🛠️ Troubleshooting</h2>
   <h3>❗ Common Issues</h3>
   <p class="first:mt-1.5"><strong class="">🐳 Docker GUI not working on Windows:</strong></p>
   <ul class="list-disc">
      <li class="ml-4">Ensure VcXsrv/Xming is running</li>
      <li class="ml-4">Check that "Disable access control" is enabled</li>
      <li class="ml-4">Verify Windows Firewall settings</li>
   </ul>
   <p class="first:mt-1.5"><strong class="">📦 Import errors:</strong></p>
   <ul class="list-disc">
      <li class="ml-4">Ensure all dependencies are installed: <code data-gramm="false">pip install -r requirements.txt</code></li>
      <li class="ml-4">Check Python version compatibility (3.10+)</li>
   </ul>
   <p class="first:mt-1.5"><strong class="">⚡ Performance issues:</strong></p>
   <ul class="list-disc">
      <li class="ml-4">Consider using GPU acceleration if available</li>
      <li class="ml-4">Increase system RAM allocation</li>
      <li class="ml-4">Close unnecessary applications</li>
   </ul>
   <h2>🤝 Contributing</h2>
   <p class="first:mt-1.5">If you would like to contribute, please follow these steps:</p>
   <ol class="list-decimal">
      <li class="ml-4"><strong class="">🍴 Fork this repository</strong></li>
      <li class="ml-4"><strong class="">🌿 Create a new branch</strong>: <code data-gramm="false">git checkout -b feature/new-feature</code></li>
      <li class="ml-4"><strong class="">✏️ Make your changes and commit them</strong>: <code data-gramm="false">git commit -m 'Add new feature'</code></li>
      <li class="ml-4"><strong class="">📤 Push your branch</strong>: <code data-gramm="false">git push origin feature/new-feature</code></li>
      <li class="ml-4"><strong class="">🔄 Open a Pull Request</strong></li>
   </ol>
   <h2>📚 Citation</h2>
   <p class="first:mt-1.5">Not publish yet.</p>
  <!-- <p class="first:mt-1.5">If you use VAP2D in your research, please cite:</p>
   <pre><div data-gramm="false" class=" relative bg-neutral-50 dark:bg-neutral-800 mb-2 rounded-[0.625rem]"><div class=" sticky top-0 bg-neutral-100 dark:bg-neutral-700 mt-[7px] rounded-t-[0.625rem] px-[14px] font-normal py-[6px] flex items-center SimTextWrite_codeHeader___xVjD justify-between">bibtex<div class="flex items-center gap-3"><div class=" flex items-center gap-[4px] text-[12px] text-darkcolor/[0.5] !cursor-pointer hover:text-darkcolor/[0.7] p-[2px] pt-[4px] rounded "><svg aria-hidden="true" focusable="false" data-prefix="far" data-icon="copy" class="svg-inline--fa fa-copy " role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M384 336H192c-8.8 0-16-7.2-16-16V64c0-8.8 7.2-16 16-16l140.1 0L400 115.9V320c0 8.8-7.2 16-16 16zM192 384H384c35.3 0 64-28.7 64-64V115.9c0-12.7-5.1-24.9-14.1-33.9L366.1 14.1c-9-9-21.2-14.1-33.9-14.1H192c-35.3 0-64 28.7-64 64V320c0 35.3 28.7 64 64 64zM64 128c-35.3 0-64 28.7-64 64V448c0 35.3 28.7 64 64 64H256c35.3 0 64-28.7 64-64V416H272v32c0 8.8-7.2 16-16 16H64c-8.8 0-16-7.2-16-16V192c0-8.8 7.2-16 16-16H96V128H64z"></path></svg><span class="w-[40px]">Copy</span></div></div></div><div class="px-[15px] py-[10px] rounded-b-[4px]" style="font-family: ui-monospace, SFMono-Regular, &quot;SF Mono&quot;, Menlo, Consolas, &quot;Liberation Mono&quot;, monospace;">@software{vap2d,  
  title={VAP2D: Visual Analysis Platform for 2D Data},  
  author={Samet Kaya},  
  year={2025},  
  url={https://github.com/sametkaya/vap2d},  
  version={v2.1}  
}  -->
</div></div></pre>
   <h2>📄 License</h2>
   <p class="first:mt-1.5">This project is licensed under the <a href="LICENSE" target="_blank" rel="noopener noreferrer" class="break-word">GNU General Public License v3.0</a>. For more details, see the <code data-gramm="false">LICENSE</code> file.</p>
   <h2>📞 Contact</h2>
   <ul class="list-disc">
      <li class="ml-4"><strong class="">👨‍💻 Author</strong>: Samet Kaya</li>
      <li class="ml-4"><strong class="">🐙 GitHub</strong>: <a href="https://github.com/sametkaya" target="_blank" rel="noopener noreferrer" class="break-word">@sametkaya</a></li>
      <li class="ml-4"><strong class="">🐳 Docker Hub</strong>: <a href="https://hub.docker.com/r/sametkaya/vap2d" target="_blank" rel="noopener noreferrer" class="break-word">sametkaya/vap2d</a></li>
   </ul>
   <p class="first:mt-1.5">For questions, suggestions, or support, please open an issue on GitHub.</p>
   <hr>
   <p class="first:mt-1.5"><strong class="">🎯 VAP2D</strong> - Making 2D data analysis accessible, reproducible, and efficient through modern software engineering practices.</p>
</span>
---
This project is designed to simplify 2D data analysis and visualization processes. We welcome your contributions and feedback!
