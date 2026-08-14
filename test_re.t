An output line can be a regular expression, and will match any output matching the regular expression
  $ echo "Ok bob"
  Ok ... (re)
  $ echo "Ok bob"
  Ok [a-z]{3} (re)
  $ echo "Foobar"
  .* (re)
  $ echo "Edge case (re)"
  Edge case (re)
  $ echo "Edge case .* (re)"
  Edge case .* (re)
  $ echo "Edge case .* (re)"
  Edge case .* (re)
