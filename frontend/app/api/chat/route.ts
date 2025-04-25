import { NextResponse } from "next/server"

export async function POST(req: Request) {
  const { messages, type } = await req.json()
  const lastUserMessage = messages[messages.length - 1].content

  try {
    const response = await fetch("http://localhost:8000/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: lastUserMessage,
        type: type || "DEFAULT",
      }),
    })

    if (!response.ok) {
      throw new Error(`Erro no backend: ${response.status}`)
    }

    const data = await response.json()

    return NextResponse.json({ response: data.response })
  } catch (error) {
    console.error("Erro ao chamar o backend:", error)
    return NextResponse.json(
      {
        response: "Desculpe, ocorreu um erro ao processar sua solicitação.",
      },
      { status: 500 }
    )
  }
}
