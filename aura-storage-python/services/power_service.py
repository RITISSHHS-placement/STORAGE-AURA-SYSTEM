BATCH_SIZE_KB = 4096
BATCH_TIMEOUT_MS = 500
POWER = {"Active": 2.3, "Idle": 1.2, "Light Sleep": 0.5, "Deep Sleep": 0.1}


class PowerService:
    def __init__(self):
        self.reset()

    def reset(self):
        self.sim_time_ms = 0
        self.aura_buffer_kb = 0.0
        self.aura_timer = 0
        self.baseline_state = "Deep Sleep"
        self.baseline_timer = 0
        self.total_baseline_energy = 0.0
        self.total_aura_energy = 0.0
        self.baseline_log = [{"time": 0, "state": "Deep Sleep", "power": 0.1}]
        self.aura_log = [{"time": 0, "state": "Deep Sleep", "power": 0.1}]
        self.events = []

    def simulate_write(self, size_kb: int) -> dict:
        self.sim_time_ms += 10

        # ── AURA logic ──────────────────────────────────────────────────────
        self.aura_timer += 10
        if size_kb > 0:
            self.aura_buffer_kb += size_kb

        buffer_full = self.aura_buffer_kb >= BATCH_SIZE_KB
        timer_expired = self.aura_timer >= BATCH_TIMEOUT_MS

        if (buffer_full or timer_expired) and self.aura_buffer_kb > 0:
            reason = "Buffer Full (4MB)" if buffer_full else "Timer Expired (500ms)"
            self.events.append(f"[{self.sim_time_ms}ms] AURA ACTIVE — {reason} — Flushing {self.aura_buffer_kb:.0f}KB")
            self._add_log(self.aura_log, self.sim_time_ms, "Active")
            self._add_log(self.aura_log, self.sim_time_ms + 200, "Deep Sleep")
            self.aura_buffer_kb = 0
            self.aura_timer = 0
            self.total_aura_energy += POWER["Active"] * 200
        else:
            self.total_aura_energy += POWER["Deep Sleep"] * 10

        # ── Baseline logic ───────────────────────────────────────────────────
        self.baseline_timer += 10
        if size_kb > 0:
            self._add_log(self.baseline_log, self.sim_time_ms, "Active")
            self.baseline_state = "Active"
            self.baseline_timer = 0
            self.events.append(f"[{self.sim_time_ms}ms] Baseline ACTIVE — writing {size_kb}KB")
            self.total_baseline_energy += POWER["Active"] * 10
        else:
            self.total_baseline_energy += POWER[self.baseline_state] * 10

        if self.baseline_state == "Active" and self.baseline_timer > 50:
            self._add_log(self.baseline_log, self.sim_time_ms, "Idle")
            self.baseline_state = "Idle"; self.baseline_timer = 0
        elif self.baseline_state == "Idle" and self.baseline_timer > 1000:
            self._add_log(self.baseline_log, self.sim_time_ms, "Light Sleep")
            self.baseline_state = "Light Sleep"; self.baseline_timer = 0
        elif self.baseline_state == "Light Sleep" and self.baseline_timer > 2000:
            self._add_log(self.baseline_log, self.sim_time_ms, "Deep Sleep")
            self.baseline_state = "Deep Sleep"; self.baseline_timer = 0

        aura_state = self.aura_log[-1]["state"] if self.aura_log else "Deep Sleep"
        savings = round((1.0 - self.total_aura_energy / max(self.total_baseline_energy, 1)) * 100, 1)

        return {
            "baselineState": self.baseline_state,
            "auraState": aura_state,
            "baselinePower": POWER[self.baseline_state],
            "auraPower": POWER[aura_state],
            "bufferUsedKb": round(self.aura_buffer_kb, 1),
            "bufferCapacityKb": BATCH_SIZE_KB,
            "bufferPercent": round(self.aura_buffer_kb / BATCH_SIZE_KB * 100, 1),
            "powerSavingsPercent": savings,
            "simulationTimeMs": self.sim_time_ms,
            "baselineLog": self.baseline_log[-40:],
            "auraLog": self.aura_log[-40:],
            "events": self.events[-10:],
        }

    def get_stats(self) -> dict:
        savings = round((1.0 - self.total_aura_energy / max(self.total_baseline_energy, 1)) * 100, 1)
        return {
            "simulationTimeMs": self.sim_time_ms,
            "baselineState": self.baseline_state,
            "auraBufferKb": round(self.aura_buffer_kb, 1),
            "bufferPercent": round(self.aura_buffer_kb / BATCH_SIZE_KB * 100, 1),
            "powerSavings": savings,
            "totalEvents": len(self.events),
        }

    def _add_log(self, log: list, time: int, state: str):
        if log and log[-1]["state"] == state:
            return
        if log:
            log.append({"time": time, "state": log[-1]["state"], "power": POWER[log[-1]["state"]]})
        log.append({"time": time, "state": state, "power": POWER[state]})
