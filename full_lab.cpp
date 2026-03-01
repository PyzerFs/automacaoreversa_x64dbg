#include "pluginmain.h" // cabecalho do plugin (provavelmente do x64dbg)
#include <fstream> // para manipulacao de arquivos
#include <windows.h> // funcoes de api do windows 
#include <wininet.h> // funcoes para conexao de rede (HTTP/FTP)
#pragma comment(lib,"wininet.lib") // linka automaticamente a biblioteca wininet 

PLUG_EXPORT void CBP_Hit(BP* bp) {
    CONTEXT ctx = {};   // estrutura para armazenar o contexto de execucao (registradores,etc.)
    ctx.ContextFlags = CONTEXT_ALL; // solicita todos os registradores
    GetThreadContext(GetCurrentThread(), &ctx); // obtem o contexto da thread atual

    // cria um arquivo para salvar valores dos registradores
    std::ofstream regFile("C:\\temp\\dumps\\regs.txt");
    regFile << "RAX:" << ctx.Rax << "\nRBX:" << ctx.Rbx << "\nRCX:" << ctx.Rcx << "\nRDX:" << ctx.Rdx << "\n";
    regFile.close();

    char buffer[0x100]; // buffer para armazenar dados da memoria (256 bytes)
    SIZE_T bytesRead;
    // le a memoria do processo atual, a partir do endereco de RAX
    ReadProcessMemory(GetCurrentProcess(), (LPCVOID)ctx.Rax, buffer, 0x100, &bytesRead);

    // salva o conteudo lido em um arquivo binario 
    std::ofstream memFile("C:\\temp\\dumps\\mem.bin", std::ios::binary);
    memFile.write(buffer, bytesRead);
    memFile.close();

    // Inicializa conexao HTTP
    HINTERNET hInternet = InternetOpen(L"x64dbgUpload", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    // conecta ao servidor HTTP na porta 5000
    HINTERNET hConnect = InternetConnect(hInternet, L"ip_de_acesso", 5000, NULL, NULL, INTERNET_SERVICE_HTTP, 0, 0);
    // prepara um request HTTP POST para "/upload"
    HINTERNET hRequest = HttpOpenRequest(hConnect, L"POST", L"/upload", NULL, NULL, NULL, 0, 0);
    // le novamente o arquivo de registradores 
    std::ifstream file("C:\\temp\\dumps\\regs.txt", std::ios::binary);
    // converte o conteudo do arquivo para string 
    std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
    // envia o conteudo do arquivo via POST
    HttpSendRequest(hRequest, NULL, 0, (LPVOID)content.c_str(), content.size());
    // fecha conexoes
    InternetCloseHandle(hRequest); InternetCloseHandle(hConnect); InternetCloseHandle(hInternet);
}

// funcao de inicializacao do pluggin
PLUG_EXPORT bool pluginit(PLUG_INITSTRUCT* initStruct) { AddBP("main", CBP_Hit); return true; } // Coloca breakpoint em "main" e chama CBP_Hit quando bater
PLUG_EXPORT void plugstop() {}
PLUG_EXPORT void plugsetup() {}
