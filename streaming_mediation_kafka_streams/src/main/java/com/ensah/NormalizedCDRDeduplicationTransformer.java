package com.ensah;

import com.ensah.telecom.events.NormalizedErrorCDR;
import org.apache.kafka.streams.KeyValue;
import org.apache.kafka.streams.kstream.Transformer;
import org.apache.kafka.streams.processor.ProcessorContext;
import org.apache.kafka.streams.state.WindowStore;
import org.apache.kafka.streams.state.WindowStoreIterator;

import java.time.Duration;

public class NormalizedCDRDeduplicationTransformer implements Transformer<String, NormalizedErrorCDR, KeyValue<String, NormalizedErrorCDR>> {


    private ProcessorContext context;
    private WindowStore<String, Long> eventIdStore;

    private final long leftDurationMs;
    private final long rightDurationMs;

    public NormalizedCDRDeduplicationTransformer(Duration deduplicationWindow) {
        long total = deduplicationWindow.toMillis();
        this.leftDurationMs = total / 2;
        this.rightDurationMs = total - this.leftDurationMs;
    }

    @Override
    public void init(ProcessorContext context) {
        this.context = context;
        this.eventIdStore = context.getStateStore("cdr-dedup-store");
    }

    @Override
    public KeyValue<String, NormalizedErrorCDR> transform(String key, NormalizedErrorCDR value) {
        if (key == null || value == null) return null;

        long eventTime = context.timestamp();

        boolean duplicate = isDuplicate(key, eventTime);
        if (duplicate) {
            return null; // suppress
        } else {
            rememberEvent(key, eventTime);
            return KeyValue.pair(key, value);
        }
    }

    @Override
    public void close() {

    }

    private boolean isDuplicate(String eventId, long eventTime) {
        WindowStoreIterator<Long> iterator = eventIdStore.fetch(
                eventId,
                eventTime - leftDurationMs,
                eventTime + rightDurationMs
        );
        boolean seen = iterator.hasNext();
        iterator.close();
        return seen;
    }
    private void rememberEvent(String eventId, long timestamp) {
        eventIdStore.put(eventId, timestamp, timestamp);
    }
}
