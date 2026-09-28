using System.Diagnostics;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace AiroRobloxBuilder;

public partial class MainWindow : Window
{
    private Process? _ai;
    private readonly string _requestPrefix = Guid.NewGuid().ToString("N");
    private int _requestNumber;

    public MainWindow()
    {
        InitializeComponent();
        AddMessage("builder", "what are we building?");
        StartAiRuntime();
    }

    private void StartAiRuntime()
    {
        try
        {
            var python = Environment.GetEnvironmentVariable("AIRO_PYTHON") ?? "python";
            _ai = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = python,
                    Arguments = "-u -m runtime",
                    WorkingDirectory = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "src", "ai")),
                    UseShellExecute = false,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                },
                EnableRaisingEvents = true
            };
            _ai.StartInfo.Environment["PYTHONPATH"] = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "src", "ai"));
            _ai.OutputDataReceived += (_, e) => { if (e.Data is not null) Dispatcher.Invoke(() => HandleAiEvent(e.Data)); };
            _ai.ErrorDataReceived += (_, e) => { if (e.Data is not null) Dispatcher.Invoke(() => AddMessage("runtime", e.Data)); };
            _ai.Start();
            _ai.BeginOutputReadLine();
            _ai.BeginErrorReadLine();
            AddMessage("runtime", "ai runtime started. configure AIRO_API_URL and AIRO_MODEL to connect a real model.");
        }
        catch (Exception ex)
        {
            AddMessage("runtime", $"could not start ai runtime: {ex.Message}");
        }
    }

    private void HandleAiEvent(string line)
    {
        try
        {
            using var doc = JsonDocument.Parse(line);
            var root = doc.RootElement;
            var type = root.GetProperty("type").GetString();
            var message = root.TryGetProperty("message", out var m) ? m.GetString() ?? "" : "";
            if (type == "text" || type == "error" || type == "complete") AddMessage(type == "error" ? "runtime" : "builder", message);
        }
        catch { }
    }

    private void Send_Click(object sender, RoutedEventArgs e) => SendPrompt();

    private void PromptBox_KeyDown(object sender, System.Windows.Input.KeyEventArgs e)
    {
        if (e.Key == System.Windows.Input.Key.Enter && !System.Windows.Input.Keyboard.Modifiers.HasFlag(System.Windows.Input.ModifierKeys.Shift))
        {
            e.Handled = true;
            SendPrompt();
        }
    }

    private void SendPrompt()
    {
        var text = PromptBox.Text.Trim();
        if (string.IsNullOrWhiteSpace(text) || text.StartsWith("describe your game")) return;
        AddMessage("you", text);
        PromptBox.Clear();
        if (_ai is null || _ai.HasExited)
        {
            AddMessage("runtime", "ai runtime is not running.");
            return;
        }
        var requestId = $"{_requestPrefix}-{++_requestNumber}";
        var payload = JsonSerializer.Serialize(new { request_id = requestId, text });
        _ai.StandardInput.WriteLine(payload);
        _ai.StandardInput.Flush();
    }

    private void AddMessage(string speaker, string text)
    {
        var panel = new StackPanel { Margin = new Thickness(0, 0, 0, 18) };
        panel.Children.Add(new TextBlock { Text = speaker, FontWeight = FontWeights.SemiBold, Foreground = speaker == "you" ? Brushes.LightSkyBlue : Brushes.LightGreen });
        panel.Children.Add(new TextBlock { Text = text, TextWrapping = TextWrapping.Wrap, FontSize = 15, Margin = new Thickness(0, 4, 0, 0) });
        ChatMessages.Children.Add(panel);
    }

    protected override void OnClosed(EventArgs e)
    {
        try { if (_ai is { HasExited: false }) { _ai.StandardInput.Close(); _ai.Kill(true); } } catch { }
        _ai?.Dispose();
        base.OnClosed(e);
    }
}
