using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
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
        AddMessage("airobloxbuilder", "what are we building?");
        StartAiRuntime();
    }

    private void ExtraButton_Click(object sender, RoutedEventArgs e) => ExtrasPopup.IsOpen = !ExtrasPopup.IsOpen;
    private void ExtraProjects_Click(object sender, RoutedEventArgs e) => AddMessage("projects", "project browser is coming online. the current project is my zombie mall.");
    private void ExtraTasks_Click(object sender, RoutedEventArgs e) => AddMessage("tasks", "no active tasks yet.");

    private void StartAiRuntime()
    {
        try
        {
            var python = Environment.GetEnvironmentVariable("AIRO_PYTHON") ?? "python";
            var runtimeDir = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", "src", "ai"));
            _ai = new Process { StartInfo = new ProcessStartInfo {
                FileName = python, Arguments = "-u -m runtime", WorkingDirectory = runtimeDir,
                UseShellExecute = false, RedirectStandardInput = true, RedirectStandardOutput = true,
                RedirectStandardError = true, CreateNoWindow = true }, EnableRaisingEvents = true };
            _ai.StartInfo.Environment["PYTHONPATH"] = runtimeDir;
            _ai.OutputDataReceived += (_, e) => { if (e.Data is not null) Dispatcher.Invoke(() => HandleAiEvent(e.Data)); };
            _ai.ErrorDataReceived += (_, e) => { if (e.Data is not null) Dispatcher.Invoke(() => AddMessage("runtime", e.Data)); };
            _ai.Start(); _ai.BeginOutputReadLine(); _ai.BeginErrorReadLine();
        }
        catch (Exception ex) { AddMessage("runtime", $"could not start ai runtime: {ex.Message}"); }
    }

    private void HandleAiEvent(string line)
    {
        try
        {
            using var doc = JsonDocument.Parse(line);
            var root = doc.RootElement;
            var type = root.GetProperty("type").GetString() ?? "";
            var message = root.TryGetProperty("message", out var m) ? m.GetString() ?? "" : "";
            if (type == "progress") AddThinking(message, "🧠");
            else if (type == "route")
            {
                var agents = root.TryGetProperty("agents", out var a) ? string.Join(", ", a.EnumerateArray().Select(x => x.GetString())) : message;
                AddThinking($"working with {agents}", "✨");
            }
            else if (type == "text") AddMessage("airobloxbuilder", message);
            else if (type == "error") AddMessage("runtime", message);
            else if (type == "complete") AddThinking("✓ finished", "✨");
        }
        catch { }
    }

    private void Send_Click(object sender, RoutedEventArgs e) => SendPrompt();

    private void PromptBox_KeyDown(object sender, KeyEventArgs e)
    {
        if (e.Key == Key.Enter && !Keyboard.Modifiers.HasFlag(ModifierKeys.Shift)) { e.Handled = true; SendPrompt(); }
    }

    private void SendPrompt()
    {
        var text = PromptBox.Text.Trim();
        if (string.IsNullOrWhiteSpace(text) || text == "tell airo what to build...") return;
        AddMessage("you", text); PromptBox.Clear();
        if (_ai is null || _ai.HasExited) { AddMessage("runtime", "ai runtime is not running."); return; }
        var payload = JsonSerializer.Serialize(new { request_id = $"{_requestPrefix}-{++_requestNumber}", text });
        _ai.StandardInput.WriteLine(payload); _ai.StandardInput.Flush();
    }

    private void AddThinking(string text, string icon)
    {
        var panel = new Border { Background = new SolidColorBrush(Color.FromRgb(20, 25, 37)), CornerRadius = new CornerRadius(14), Padding = new Thickness(15), Margin = new Thickness(0, 0, 0, 12) };
        var stack = new StackPanel();
        stack.Children.Add(new TextBlock { Text = $"{icon}  {text}", FontWeight = FontWeights.SemiBold, Foreground = new SolidColorBrush(Color.FromRgb(183, 151, 255)) });
        stack.Children.Add(new TextBlock { Text = "●  ●  ●", Foreground = new SolidColorBrush(Color.FromRgb(111, 122, 141)), FontSize = 11, Margin = new Thickness(0, 6, 0, 0) });
        panel.Child = stack; ChatMessages.Children.Add(panel);
    }

    private void AddMessage(string speaker, string text)
    {
        var panel = new StackPanel { Margin = new Thickness(0, 0, 0, 22) };
        panel.Children.Add(new TextBlock { Text = speaker, FontWeight = FontWeights.SemiBold, Foreground = speaker == "you" ? new SolidColorBrush(Color.FromRgb(119, 200, 255)) : new SolidColorBrush(Color.FromRgb(117, 230, 165)) });
        panel.Children.Add(new TextBlock { Text = text, TextWrapping = TextWrapping.Wrap, FontSize = 15, Margin = new Thickness(0, 5, 0, 0) });
        ChatMessages.Children.Add(panel);
    }

    protected override void OnClosed(EventArgs e)
    {
        try { if (_ai is { HasExited: false }) { _ai.StandardInput.Close(); _ai.Kill(true); } } catch { }
        _ai?.Dispose(); base.OnClosed(e);
    }
}