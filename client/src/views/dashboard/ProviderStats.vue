<script setup>
import Card from "@/components/Card.vue";
</script>

<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 w-full">
    <Card class="min-h-[120px] flex flex-col items-center justify-center">
      <h2 class="font-semibold text-lg mb-1 text-center">Total Data Sources</h2>
      <p class="text-3xl text-center">6</p>
    </Card>

    <Card class="min-h-[120px] flex flex-col items-center justify-center">
      <h2 class="font-semibold text-lg mb-1 text-center">Error Stats</h2>
      <p class="text-3xl text-center text-nord11">
        3 failed
        <br />
        <span class="text-base text-nord12">0.2% error rate</span>
      </p>
    </Card>

    <Card class="min-h-[120px] flex flex-col items-center justify-center">
      <h2 class="font-semibold text-lg mb-1 text-center">Usage Trends</h2>
      <p class="text-3xl text-center">
        120/min
        <br />
        <span class="text-base text-nord10">+8% this week</span>
      </p>
    </Card>

    <Card class="min-h-[120px] flex flex-col items-center justify-center">
      <h2 class="font-semibold text-lg mb-1 text-center">Alerts</h2>
      <p class="text-3xl text-center text-nord13">2</p>
      <span class="text-base text-nord11">Failed ingestion, backlog</span>
    </Card>
  </div>
</template>
