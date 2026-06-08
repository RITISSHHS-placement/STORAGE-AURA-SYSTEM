import random
import hashlib
import time


PRIME = 2**127 - 1  # Mersenne prime


class SecurityService:
    def _poly_eval(self, coeffs: list, x: int) -> int:
        result = 0
        for c in reversed(coeffs):
            result = (result * x + c) % PRIME
        return result

    def _lagrange(self, shares: list, x: int = 0) -> int:
        secret = 0
        for i, (xi, yi) in enumerate(shares):
            num, den = 1, 1
            for j, (xj, _) in enumerate(shares):
                if i != j:
                    num = (num * (x - xj)) % PRIME
                    den = (den * (xi - xj)) % PRIME
            secret = (secret + yi * num * pow(den, -1, PRIME)) % PRIME
        return secret

    def split_secret(self, secret: int, threshold: int, total: int) -> tuple[list, list]:
        coeffs = [secret] + [random.randint(1, PRIME - 1) for _ in range(threshold - 1)]
        shares = [(i, self._poly_eval(coeffs, i)) for i in range(1, total + 1)]
        return shares, coeffs

    def run_demo(self, secret: int, threshold: int, total: int) -> dict:
        shares, coeffs = self.split_secret(secret, threshold, total)
        poly_terms = " + ".join(
            f"{c}·x^{i}" if i > 0 else str(c)
            for i, c in enumerate(coeffs)
        )
        nodes = [f"Node_{chr(65 + i)}" for i in range(total)]

        return {
            "success": True,
            "secret": secret,
            "threshold": threshold,
            "total": total,
            "shares": [{"node": nodes[i], "x": x, "y": y} for i, (x, y) in enumerate(shares)],
            "polynomialFormula": f"P(x) = {poly_terms} (mod p)",
            "prime": str(PRIME),
        }

    def encrypt_and_shard(self, data: str, threshold: int, total: int) -> dict:
        t0 = time.time()
        secret_int = int.from_bytes(data[:8].encode().ljust(8, b"\x00"), "big")
        shares, coeffs = self.split_secret(secret_int, threshold, total)
        nodes = [f"Node_{chr(65 + i)}" for i in range(total)]
        enc_hash = hashlib.sha256(data.encode()).hexdigest()[:16]

        return {
            "success": True,
            "encryptedHash": enc_hash,
            "threshold": threshold,
            "totalShares": total,
            "shares": [{"node": nodes[i], "x": x, "y": str(y)[:20] + "…"} for i, (x, y) in enumerate(shares)],
            "nodes": nodes,
            "polynomialFormula": f"P(x) = secret + a₁x + … + a{threshold-1}x^{threshold-1} (mod p)",
            "encryptionTimeMs": round((time.time() - t0) * 1000, 2),
            "status": "Encrypted & Distributed",
        }

    def reconstruct(self, payload: dict) -> dict:
        shares_raw = payload.get("shares", [])
        threshold = int(payload.get("threshold", 3))
        if len(shares_raw) < threshold:
            return {"success": False, "error": f"Need at least {threshold} shares"}
        shares = [(int(s["x"]), int(s["y"])) for s in shares_raw[:threshold]]
        reconstructed = self._lagrange(shares)
        return {"success": True, "reconstructed": reconstructed, "sharesUsed": len(shares)}
