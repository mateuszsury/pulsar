import { useEffect, useCallback, useRef } from 'react'
import { websocket, WebSocketMessage } from '../services/websocket'
import { useDeviceStore } from '../stores/deviceStore'
import { useConsoleStore } from '../stores/consoleStore'

export function useWebSocket() {
  const { updateDevice, removeDevice, fetchPorts } = useDeviceStore()
  const { appendOutput } = useConsoleStore()
  const isConnected = useRef(false)

  const connect = useCallback(async () => {
    if (isConnected.current) return

    try {
      await websocket.connect()
      isConnected.current = true
    } catch (error) {
      console.error('WebSocket connection failed:', error)
    }
  }, [])

  useEffect(() => {
    // Debug: log all incoming messages
    const debugHandler = websocket.on('*', (msg: WebSocketMessage) => {
      console.log('[WS] Received:', msg.type, msg.data)
    })

    // Handle device events
    const handlers = [
      debugHandler,

      websocket.on('device:connected', (msg: WebSocketMessage) => {
        console.log('[WS] device:connected', msg.data)
        if (msg.data?.info) {
          updateDevice(msg.data.info as { port: string })
        }
      }),

      websocket.on('device:disconnected', (msg: WebSocketMessage) => {
        console.log('[WS] device:disconnected', msg.data)
        if (msg.data?.port) {
          removeDevice(msg.data.port as string)
        }
      }),

      websocket.on('device:output', (msg: WebSocketMessage) => {
        const text = msg.data?.text as string | undefined
        console.log('[WS] device:output', msg.data?.port, text?.substring(0, 50))
        if (msg.data?.port && text) {
          appendOutput(msg.data.port as string, text)
        }
      }),

      websocket.on('device:error', (msg: WebSocketMessage) => {
        console.log('[WS] device:error', msg.data)
        if (msg.data?.port) {
          updateDevice({
            port: msg.data.port as string,
            state: 'error',
            error: msg.data.error as string || 'Unknown error',
          })
        }
      }),

      websocket.on('device:reset', (msg: WebSocketMessage) => {
        console.log('[WS] device:reset', msg.data)
        const port = msg.data?.port as string
        const success = msg.data?.success as boolean
        const soft = msg.data?.soft as boolean
        if (port) {
          if (success) {
            appendOutput(port, `\r\n[${soft ? 'Soft' : 'Hard'} reset completed]\r\n`)
          } else {
            const error = msg.data?.error as string || 'Unknown error'
            appendOutput(port, `\r\n[Reset failed: ${error}]\r\n`)
          }
        }
      }),

      websocket.on('device:interrupted', (msg: WebSocketMessage) => {
        console.log('[WS] device:interrupted', msg.data)
        const port = msg.data?.port as string
        const success = msg.data?.success as boolean
        if (port) {
          if (success) {
            appendOutput(port, '\r\n[Interrupted]\r\n')
          } else {
            const error = msg.data?.error as string || 'Unknown error'
            appendOutput(port, `\r\n[Interrupt failed: ${error}]\r\n`)
          }
        }
      }),

      websocket.on('ports:updated', () => {
        console.log('[WS] ports:updated')
        fetchPorts()
      }),
    ]

    return () => {
      handlers.forEach(unsubscribe => unsubscribe())
    }
  }, [updateDevice, removeDevice, appendOutput, fetchPorts])

  const subscribe = useCallback((port: string) => {
    websocket.subscribe(port)
  }, [])

  const unsubscribe = useCallback((port: string) => {
    websocket.unsubscribe(port)
  }, [])

  const sendInput = useCallback((port: string, text: string) => {
    websocket.sendInput(port, text)
  }, [])

  return {
    connect,
    subscribe,
    unsubscribe,
    sendInput,
    isConnected: websocket.isConnected,
  }
}
