export const handler = async (event) => {
  try {
    const name = event.queryStringParameters?.name || "daniel";

    const response = await fetch(`https://api.agify.io/?name=${name}`);
    const data = await response.json();

    const claims =
      event.requestContext?.authorizer?.jwt?.claims || {};

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        external_response: data,
        authenticated_user: claims.email,
        sub: claims.sub
      })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};