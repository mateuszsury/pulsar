/**
 * WebSocket service for real-time communication
 */

export type MessageHandler = (data: WebSocketMessage) => void

export interface WebSocketMessage {
  type: string
  data?: Record<string, unknown>
  timestamp?: string
  source?: string
}

class WebSocketService {
  private ws: WebSocket | null = null
  private handlers: Map<string, Set<MessageHandler>> = new Map()
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private subscriptions: Set<string> = new Set()

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
      const host = window.location.host
      const url = `${protocol}//${host}/ws`

      try {
        this.ws = new WebSocket(url)

        this.ws.onopen = () => {
          console.log('WebSocket connected')
          this.reconnectAttempts = 0

          // Resubscribe to ports
          this.subscriptions.forEach(port => {
            this.send({ type: 'subscribe', port })
          })

          resolve()
        }

        this.ws.onmessage = (event) => {
          try {
            const message = JSON.parse(event.data) as WebSocketMessage
            this.dispatch(message)
          } catch (error) {
            console.error('Failed to parse WebSocket message:', error)
          }
        }

        this.ws.onclose = () => {
          console.log('WebSocket disconnected')
          this.scheduleReconnect()
        }

        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error)
          reject(error)
        }
      } catch (error) {
        reject(error)
      }
    })
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnect attempts reached')
      return
    }

    this.reconnectAttempts++
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1)

    console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`)

    setTimeout(() => {
      this.connect().catch(console.error)
    }, delay)
  }

  send(data: Record<string, unknown>): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data))
    }
  }

  subscribe(port: string): void {
    this.subscriptions.add(port)
    this.send({ type: 'subscribe', port })
  }

  unsubscribe(port: string): void {
    this.subscriptions.delete(port)
    this.send({ type: 'unsubscribe', port })
  }

  sendInput(port: string, text: string): void {
    this.send({ type: 'repl:input', port, text })
  }

  on(type: string, handler: MessageHandler): () => void {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set())
    }
    this.handlers.get(type)!.add(handler)

    // Return unsubscribe function
    return () => {
      this.handlers.get(type)?.delete(handler)
    }
  }

  off(type: string, handler: MessageHandler): void {
    this.handlers.get(type)?.delete(handler)
  }

  private dispatch(message: WebSocketMessage): void {
    // Call specific handlers
    const handlers = this.handlers.get(message.type)
    handlers?.forEach(handler => {
      try {
        handler(message)
      } catch (error) {
        console.error('Handler error:', error)
      }
    })

    // Call wildcard handlers
    const wildcardHandlers = this.handlers.get('*')
    wildcardHandlers?.forEach(handler => {
      try {
        handler(message)
      } catch (error) {
        console.error('Wildcard handler error:', error)
      }
    })
  }

  get isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN
  }
}

// Singleton instance
export const websocket = new WebSocketService()
