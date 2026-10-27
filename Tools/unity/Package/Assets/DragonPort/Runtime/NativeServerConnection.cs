using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;

// Attach to a GameObject. Requires a running run_unity_gateway.py process.
public sealed class NativeServerConnection : MonoBehaviour
{
    public string Host = "127.0.0.1";
    public int Port = 15800;
    private TcpClient client;
    private bool destroyed;

    [Serializable] private sealed class Request
    {
        public int v = 1;
        public string id;
        public string method;
    }

    [Serializable] private sealed class Response
    {
        public int v;
        public string id;
        public bool ok;
    }

    private async void Start()
    {
        try
        {
            client = new TcpClient();
            var connect = client.ConnectAsync(Host, Port);
            if (await Task.WhenAny(connect, Task.Delay(5000)) != connect)
                throw new TimeoutException("Server connection timed out");
            await connect;
            if (destroyed) return;
            using (var stream = client.GetStream())
            using (var reader = new StreamReader(stream, new UTF8Encoding(false)))
            using (var writer = new StreamWriter(stream, new UTF8Encoding(false)) { AutoFlush = true, NewLine = "\n" })
            {
                foreach (var method in new[] { "hello", "ping" })
                {
                    var request = new Request { id = Guid.NewGuid().ToString("N"), method = method };
                    await writer.WriteLineAsync(JsonUtility.ToJson(request));
                    var read = reader.ReadLineAsync();
                    if (await Task.WhenAny(read, Task.Delay(5000)) != read)
                        throw new TimeoutException("Server response timed out");
                    var response = await read;
                    if (response == null) throw new IOException("Server closed the connection");
                    var envelope = JsonUtility.FromJson<Response>(response);
                    if (envelope == null || envelope.v != 1 || envelope.id != request.id || !envelope.ok)
                        throw new IOException("Invalid or unsuccessful server response: " + response);
                    if (!destroyed) Debug.Log("Native server: " + response);
                }
            }
        }
        catch (Exception error)
        {
            if (!destroyed) Debug.LogError("Native server connection: " + error.Message);
        }
        finally { client?.Close(); }
    }

    private void OnDestroy()
    {
        destroyed = true;
        client?.Close();
    }
}
