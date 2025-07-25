/**
 * Autogenerated by Avro
 *
 * DO NOT EDIT DIRECTLY
 */
package com.ensah.telecom.events;

import org.apache.avro.specific.SpecificData;
import org.apache.avro.util.Utf8;
import org.apache.avro.message.BinaryMessageEncoder;
import org.apache.avro.message.BinaryMessageDecoder;
import org.apache.avro.message.SchemaStore;

@org.apache.avro.specific.AvroGenerated
public class NormalizedErrorCDR extends org.apache.avro.specific.SpecificRecordBase implements org.apache.avro.specific.SpecificRecord {
  private static final long serialVersionUID = 8548476016705432835L;


  public static final org.apache.avro.Schema SCHEMA$ = new org.apache.avro.Schema.Parser().parse("{\"type\":\"record\",\"name\":\"NormalizedErrorCDR\",\"namespace\":\"com.ensah.telecom.events\",\"fields\":[{\"name\":\"uuid\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"record_type\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"timestamp\",\"type\":[\"null\",{\"type\":\"long\",\"logicalType\":\"timestamp-millis\"}],\"default\":null},{\"name\":\"msisdn\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"counterparty_msisdn\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"duration_sec\",\"type\":[\"null\",\"int\"],\"default\":null},{\"name\":\"data_volume_mb\",\"type\":[\"null\",\"double\"],\"default\":null},{\"name\":\"cell_id\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"technology\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"status\",\"type\":[\"null\",\"string\"],\"default\":null}]}");
  public static org.apache.avro.Schema getClassSchema() { return SCHEMA$; }

  private static final SpecificData MODEL$ = new SpecificData();
  static {
    MODEL$.addLogicalTypeConversion(new org.apache.avro.data.TimeConversions.TimestampMillisConversion());
  }

  private static final BinaryMessageEncoder<NormalizedErrorCDR> ENCODER =
      new BinaryMessageEncoder<>(MODEL$, SCHEMA$);

  private static final BinaryMessageDecoder<NormalizedErrorCDR> DECODER =
      new BinaryMessageDecoder<>(MODEL$, SCHEMA$);

  /**
   * Return the BinaryMessageEncoder instance used by this class.
   * @return the message encoder used by this class
   */
  public static BinaryMessageEncoder<NormalizedErrorCDR> getEncoder() {
    return ENCODER;
  }

  /**
   * Return the BinaryMessageDecoder instance used by this class.
   * @return the message decoder used by this class
   */
  public static BinaryMessageDecoder<NormalizedErrorCDR> getDecoder() {
    return DECODER;
  }

  /**
   * Create a new BinaryMessageDecoder instance for this class that uses the specified {@link SchemaStore}.
   * @param resolver a {@link SchemaStore} used to find schemas by fingerprint
   * @return a BinaryMessageDecoder instance for this class backed by the given SchemaStore
   */
  public static BinaryMessageDecoder<NormalizedErrorCDR> createDecoder(SchemaStore resolver) {
    return new BinaryMessageDecoder<>(MODEL$, SCHEMA$, resolver);
  }

  /**
   * Serializes this NormalizedErrorCDR to a ByteBuffer.
   * @return a buffer holding the serialized data for this instance
   * @throws java.io.IOException if this instance could not be serialized
   */
  public java.nio.ByteBuffer toByteBuffer() throws java.io.IOException {
    return ENCODER.encode(this);
  }

  /**
   * Deserializes a NormalizedErrorCDR from a ByteBuffer.
   * @param b a byte buffer holding serialized data for an instance of this class
   * @return a NormalizedErrorCDR instance decoded from the given buffer
   * @throws java.io.IOException if the given bytes could not be deserialized into an instance of this class
   */
  public static NormalizedErrorCDR fromByteBuffer(
      java.nio.ByteBuffer b) throws java.io.IOException {
    return DECODER.decode(b);
  }

  private java.lang.CharSequence uuid;
  private java.lang.CharSequence record_type;
  private java.time.Instant timestamp;
  private java.lang.CharSequence msisdn;
  private java.lang.CharSequence counterparty_msisdn;
  private java.lang.Integer duration_sec;
  private java.lang.Double data_volume_mb;
  private java.lang.CharSequence cell_id;
  private java.lang.CharSequence technology;
  private java.lang.CharSequence status;

  /**
   * Default constructor.  Note that this does not initialize fields
   * to their default values from the schema.  If that is desired then
   * one should use <code>newBuilder()</code>.
   */
  public NormalizedErrorCDR() {}

  /**
   * All-args constructor.
   * @param uuid The new value for uuid
   * @param record_type The new value for record_type
   * @param timestamp The new value for timestamp
   * @param msisdn The new value for msisdn
   * @param counterparty_msisdn The new value for counterparty_msisdn
   * @param duration_sec The new value for duration_sec
   * @param data_volume_mb The new value for data_volume_mb
   * @param cell_id The new value for cell_id
   * @param technology The new value for technology
   * @param status The new value for status
   */
  public NormalizedErrorCDR(java.lang.CharSequence uuid, java.lang.CharSequence record_type, java.time.Instant timestamp, java.lang.CharSequence msisdn, java.lang.CharSequence counterparty_msisdn, java.lang.Integer duration_sec, java.lang.Double data_volume_mb, java.lang.CharSequence cell_id, java.lang.CharSequence technology, java.lang.CharSequence status) {
    this.uuid = uuid;
    this.record_type = record_type;
    this.timestamp = timestamp;
    this.msisdn = msisdn;
    this.counterparty_msisdn = counterparty_msisdn;
    this.duration_sec = duration_sec;
    this.data_volume_mb = data_volume_mb;
    this.cell_id = cell_id;
    this.technology = technology;
    this.status = status;
  }

  @Override
  public org.apache.avro.specific.SpecificData getSpecificData() { return MODEL$; }

  @Override
  public org.apache.avro.Schema getSchema() { return SCHEMA$; }

  // Used by DatumWriter.  Applications should not call.
  @Override
  public java.lang.Object get(int field$) {
    switch (field$) {
    case 0: return uuid;
    case 1: return record_type;
    case 2: return timestamp;
    case 3: return msisdn;
    case 4: return counterparty_msisdn;
    case 5: return duration_sec;
    case 6: return data_volume_mb;
    case 7: return cell_id;
    case 8: return technology;
    case 9: return status;
    default: throw new IndexOutOfBoundsException("Invalid index: " + field$);
    }
  }

  // Used by DatumReader.  Applications should not call.
  @Override
  @SuppressWarnings(value="unchecked")
  public void put(int field$, java.lang.Object value$) {
    switch (field$) {
    case 0: uuid = (java.lang.CharSequence)value$; break;
    case 1: record_type = (java.lang.CharSequence)value$; break;
    case 2: timestamp = (java.time.Instant)value$; break;
    case 3: msisdn = (java.lang.CharSequence)value$; break;
    case 4: counterparty_msisdn = (java.lang.CharSequence)value$; break;
    case 5: duration_sec = (java.lang.Integer)value$; break;
    case 6: data_volume_mb = (java.lang.Double)value$; break;
    case 7: cell_id = (java.lang.CharSequence)value$; break;
    case 8: technology = (java.lang.CharSequence)value$; break;
    case 9: status = (java.lang.CharSequence)value$; break;
    default: throw new IndexOutOfBoundsException("Invalid index: " + field$);
    }
  }

  /**
   * Gets the value of the 'uuid' field.
   * @return The value of the 'uuid' field.
   */
  public java.lang.CharSequence getUuid() {
    return uuid;
  }


  /**
   * Sets the value of the 'uuid' field.
   * @param value the value to set.
   */
  public void setUuid(java.lang.CharSequence value) {
    this.uuid = value;
  }

  /**
   * Gets the value of the 'record_type' field.
   * @return The value of the 'record_type' field.
   */
  public java.lang.CharSequence getRecordType() {
    return record_type;
  }


  /**
   * Sets the value of the 'record_type' field.
   * @param value the value to set.
   */
  public void setRecordType(java.lang.CharSequence value) {
    this.record_type = value;
  }

  /**
   * Gets the value of the 'timestamp' field.
   * @return The value of the 'timestamp' field.
   */
  public java.time.Instant getTimestamp() {
    return timestamp;
  }


  /**
   * Sets the value of the 'timestamp' field.
   * @param value the value to set.
   */
  public void setTimestamp(java.time.Instant value) {
    this.timestamp = value;
  }

  /**
   * Gets the value of the 'msisdn' field.
   * @return The value of the 'msisdn' field.
   */
  public java.lang.CharSequence getMsisdn() {
    return msisdn;
  }


  /**
   * Sets the value of the 'msisdn' field.
   * @param value the value to set.
   */
  public void setMsisdn(java.lang.CharSequence value) {
    this.msisdn = value;
  }

  /**
   * Gets the value of the 'counterparty_msisdn' field.
   * @return The value of the 'counterparty_msisdn' field.
   */
  public java.lang.CharSequence getCounterpartyMsisdn() {
    return counterparty_msisdn;
  }


  /**
   * Sets the value of the 'counterparty_msisdn' field.
   * @param value the value to set.
   */
  public void setCounterpartyMsisdn(java.lang.CharSequence value) {
    this.counterparty_msisdn = value;
  }

  /**
   * Gets the value of the 'duration_sec' field.
   * @return The value of the 'duration_sec' field.
   */
  public java.lang.Integer getDurationSec() {
    return duration_sec;
  }


  /**
   * Sets the value of the 'duration_sec' field.
   * @param value the value to set.
   */
  public void setDurationSec(java.lang.Integer value) {
    this.duration_sec = value;
  }

  /**
   * Gets the value of the 'data_volume_mb' field.
   * @return The value of the 'data_volume_mb' field.
   */
  public java.lang.Double getDataVolumeMb() {
    return data_volume_mb;
  }


  /**
   * Sets the value of the 'data_volume_mb' field.
   * @param value the value to set.
   */
  public void setDataVolumeMb(java.lang.Double value) {
    this.data_volume_mb = value;
  }

  /**
   * Gets the value of the 'cell_id' field.
   * @return The value of the 'cell_id' field.
   */
  public java.lang.CharSequence getCellId() {
    return cell_id;
  }


  /**
   * Sets the value of the 'cell_id' field.
   * @param value the value to set.
   */
  public void setCellId(java.lang.CharSequence value) {
    this.cell_id = value;
  }

  /**
   * Gets the value of the 'technology' field.
   * @return The value of the 'technology' field.
   */
  public java.lang.CharSequence getTechnology() {
    return technology;
  }


  /**
   * Sets the value of the 'technology' field.
   * @param value the value to set.
   */
  public void setTechnology(java.lang.CharSequence value) {
    this.technology = value;
  }

  /**
   * Gets the value of the 'status' field.
   * @return The value of the 'status' field.
   */
  public java.lang.CharSequence getStatus() {
    return status;
  }


  /**
   * Sets the value of the 'status' field.
   * @param value the value to set.
   */
  public void setStatus(java.lang.CharSequence value) {
    this.status = value;
  }

  /**
   * Creates a new NormalizedErrorCDR RecordBuilder.
   * @return A new NormalizedErrorCDR RecordBuilder
   */
  public static com.ensah.telecom.events.NormalizedErrorCDR.Builder newBuilder() {
    return new com.ensah.telecom.events.NormalizedErrorCDR.Builder();
  }

  /**
   * Creates a new NormalizedErrorCDR RecordBuilder by copying an existing Builder.
   * @param other The existing builder to copy.
   * @return A new NormalizedErrorCDR RecordBuilder
   */
  public static com.ensah.telecom.events.NormalizedErrorCDR.Builder newBuilder(com.ensah.telecom.events.NormalizedErrorCDR.Builder other) {
    if (other == null) {
      return new com.ensah.telecom.events.NormalizedErrorCDR.Builder();
    } else {
      return new com.ensah.telecom.events.NormalizedErrorCDR.Builder(other);
    }
  }

  /**
   * Creates a new NormalizedErrorCDR RecordBuilder by copying an existing NormalizedErrorCDR instance.
   * @param other The existing instance to copy.
   * @return A new NormalizedErrorCDR RecordBuilder
   */
  public static com.ensah.telecom.events.NormalizedErrorCDR.Builder newBuilder(com.ensah.telecom.events.NormalizedErrorCDR other) {
    if (other == null) {
      return new com.ensah.telecom.events.NormalizedErrorCDR.Builder();
    } else {
      return new com.ensah.telecom.events.NormalizedErrorCDR.Builder(other);
    }
  }

  /**
   * RecordBuilder for NormalizedErrorCDR instances.
   */
  @org.apache.avro.specific.AvroGenerated
  public static class Builder extends org.apache.avro.specific.SpecificRecordBuilderBase<NormalizedErrorCDR>
    implements org.apache.avro.data.RecordBuilder<NormalizedErrorCDR> {

    private java.lang.CharSequence uuid;
    private java.lang.CharSequence record_type;
    private java.time.Instant timestamp;
    private java.lang.CharSequence msisdn;
    private java.lang.CharSequence counterparty_msisdn;
    private java.lang.Integer duration_sec;
    private java.lang.Double data_volume_mb;
    private java.lang.CharSequence cell_id;
    private java.lang.CharSequence technology;
    private java.lang.CharSequence status;

    /** Creates a new Builder */
    private Builder() {
      super(SCHEMA$, MODEL$);
    }

    /**
     * Creates a Builder by copying an existing Builder.
     * @param other The existing Builder to copy.
     */
    private Builder(com.ensah.telecom.events.NormalizedErrorCDR.Builder other) {
      super(other);
      if (isValidValue(fields()[0], other.uuid)) {
        this.uuid = data().deepCopy(fields()[0].schema(), other.uuid);
        fieldSetFlags()[0] = other.fieldSetFlags()[0];
      }
      if (isValidValue(fields()[1], other.record_type)) {
        this.record_type = data().deepCopy(fields()[1].schema(), other.record_type);
        fieldSetFlags()[1] = other.fieldSetFlags()[1];
      }
      if (isValidValue(fields()[2], other.timestamp)) {
        this.timestamp = data().deepCopy(fields()[2].schema(), other.timestamp);
        fieldSetFlags()[2] = other.fieldSetFlags()[2];
      }
      if (isValidValue(fields()[3], other.msisdn)) {
        this.msisdn = data().deepCopy(fields()[3].schema(), other.msisdn);
        fieldSetFlags()[3] = other.fieldSetFlags()[3];
      }
      if (isValidValue(fields()[4], other.counterparty_msisdn)) {
        this.counterparty_msisdn = data().deepCopy(fields()[4].schema(), other.counterparty_msisdn);
        fieldSetFlags()[4] = other.fieldSetFlags()[4];
      }
      if (isValidValue(fields()[5], other.duration_sec)) {
        this.duration_sec = data().deepCopy(fields()[5].schema(), other.duration_sec);
        fieldSetFlags()[5] = other.fieldSetFlags()[5];
      }
      if (isValidValue(fields()[6], other.data_volume_mb)) {
        this.data_volume_mb = data().deepCopy(fields()[6].schema(), other.data_volume_mb);
        fieldSetFlags()[6] = other.fieldSetFlags()[6];
      }
      if (isValidValue(fields()[7], other.cell_id)) {
        this.cell_id = data().deepCopy(fields()[7].schema(), other.cell_id);
        fieldSetFlags()[7] = other.fieldSetFlags()[7];
      }
      if (isValidValue(fields()[8], other.technology)) {
        this.technology = data().deepCopy(fields()[8].schema(), other.technology);
        fieldSetFlags()[8] = other.fieldSetFlags()[8];
      }
      if (isValidValue(fields()[9], other.status)) {
        this.status = data().deepCopy(fields()[9].schema(), other.status);
        fieldSetFlags()[9] = other.fieldSetFlags()[9];
      }
    }

    /**
     * Creates a Builder by copying an existing NormalizedErrorCDR instance
     * @param other The existing instance to copy.
     */
    private Builder(com.ensah.telecom.events.NormalizedErrorCDR other) {
      super(SCHEMA$, MODEL$);
      if (isValidValue(fields()[0], other.uuid)) {
        this.uuid = data().deepCopy(fields()[0].schema(), other.uuid);
        fieldSetFlags()[0] = true;
      }
      if (isValidValue(fields()[1], other.record_type)) {
        this.record_type = data().deepCopy(fields()[1].schema(), other.record_type);
        fieldSetFlags()[1] = true;
      }
      if (isValidValue(fields()[2], other.timestamp)) {
        this.timestamp = data().deepCopy(fields()[2].schema(), other.timestamp);
        fieldSetFlags()[2] = true;
      }
      if (isValidValue(fields()[3], other.msisdn)) {
        this.msisdn = data().deepCopy(fields()[3].schema(), other.msisdn);
        fieldSetFlags()[3] = true;
      }
      if (isValidValue(fields()[4], other.counterparty_msisdn)) {
        this.counterparty_msisdn = data().deepCopy(fields()[4].schema(), other.counterparty_msisdn);
        fieldSetFlags()[4] = true;
      }
      if (isValidValue(fields()[5], other.duration_sec)) {
        this.duration_sec = data().deepCopy(fields()[5].schema(), other.duration_sec);
        fieldSetFlags()[5] = true;
      }
      if (isValidValue(fields()[6], other.data_volume_mb)) {
        this.data_volume_mb = data().deepCopy(fields()[6].schema(), other.data_volume_mb);
        fieldSetFlags()[6] = true;
      }
      if (isValidValue(fields()[7], other.cell_id)) {
        this.cell_id = data().deepCopy(fields()[7].schema(), other.cell_id);
        fieldSetFlags()[7] = true;
      }
      if (isValidValue(fields()[8], other.technology)) {
        this.technology = data().deepCopy(fields()[8].schema(), other.technology);
        fieldSetFlags()[8] = true;
      }
      if (isValidValue(fields()[9], other.status)) {
        this.status = data().deepCopy(fields()[9].schema(), other.status);
        fieldSetFlags()[9] = true;
      }
    }

    /**
      * Gets the value of the 'uuid' field.
      * @return The value.
      */
    public java.lang.CharSequence getUuid() {
      return uuid;
    }


    /**
      * Sets the value of the 'uuid' field.
      * @param value The value of 'uuid'.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder setUuid(java.lang.CharSequence value) {
      validate(fields()[0], value);
      this.uuid = value;
      fieldSetFlags()[0] = true;
      return this;
    }

    /**
      * Checks whether the 'uuid' field has been set.
      * @return True if the 'uuid' field has been set, false otherwise.
      */
    public boolean hasUuid() {
      return fieldSetFlags()[0];
    }


    /**
      * Clears the value of the 'uuid' field.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder clearUuid() {
      uuid = null;
      fieldSetFlags()[0] = false;
      return this;
    }

    /**
      * Gets the value of the 'record_type' field.
      * @return The value.
      */
    public java.lang.CharSequence getRecordType() {
      return record_type;
    }


    /**
      * Sets the value of the 'record_type' field.
      * @param value The value of 'record_type'.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder setRecordType(java.lang.CharSequence value) {
      validate(fields()[1], value);
      this.record_type = value;
      fieldSetFlags()[1] = true;
      return this;
    }

    /**
      * Checks whether the 'record_type' field has been set.
      * @return True if the 'record_type' field has been set, false otherwise.
      */
    public boolean hasRecordType() {
      return fieldSetFlags()[1];
    }


    /**
      * Clears the value of the 'record_type' field.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder clearRecordType() {
      record_type = null;
      fieldSetFlags()[1] = false;
      return this;
    }

    /**
      * Gets the value of the 'timestamp' field.
      * @return The value.
      */
    public java.time.Instant getTimestamp() {
      return timestamp;
    }


    /**
      * Sets the value of the 'timestamp' field.
      * @param value The value of 'timestamp'.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder setTimestamp(java.time.Instant value) {
      validate(fields()[2], value);
      this.timestamp = value;
      fieldSetFlags()[2] = true;
      return this;
    }

    /**
      * Checks whether the 'timestamp' field has been set.
      * @return True if the 'timestamp' field has been set, false otherwise.
      */
    public boolean hasTimestamp() {
      return fieldSetFlags()[2];
    }


    /**
      * Clears the value of the 'timestamp' field.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder clearTimestamp() {
      timestamp = null;
      fieldSetFlags()[2] = false;
      return this;
    }

    /**
      * Gets the value of the 'msisdn' field.
      * @return The value.
      */
    public java.lang.CharSequence getMsisdn() {
      return msisdn;
    }


    /**
      * Sets the value of the 'msisdn' field.
      * @param value The value of 'msisdn'.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder setMsisdn(java.lang.CharSequence value) {
      validate(fields()[3], value);
      this.msisdn = value;
      fieldSetFlags()[3] = true;
      return this;
    }

    /**
      * Checks whether the 'msisdn' field has been set.
      * @return True if the 'msisdn' field has been set, false otherwise.
      */
    public boolean hasMsisdn() {
      return fieldSetFlags()[3];
    }


    /**
      * Clears the value of the 'msisdn' field.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder clearMsisdn() {
      msisdn = null;
      fieldSetFlags()[3] = false;
      return this;
    }

    /**
      * Gets the value of the 'counterparty_msisdn' field.
      * @return The value.
      */
    public java.lang.CharSequence getCounterpartyMsisdn() {
      return counterparty_msisdn;
    }


    /**
      * Sets the value of the 'counterparty_msisdn' field.
      * @param value The value of 'counterparty_msisdn'.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder setCounterpartyMsisdn(java.lang.CharSequence value) {
      validate(fields()[4], value);
      this.counterparty_msisdn = value;
      fieldSetFlags()[4] = true;
      return this;
    }

    /**
      * Checks whether the 'counterparty_msisdn' field has been set.
      * @return True if the 'counterparty_msisdn' field has been set, false otherwise.
      */
    public boolean hasCounterpartyMsisdn() {
      return fieldSetFlags()[4];
    }


    /**
      * Clears the value of the 'counterparty_msisdn' field.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder clearCounterpartyMsisdn() {
      counterparty_msisdn = null;
      fieldSetFlags()[4] = false;
      return this;
    }

    /**
      * Gets the value of the 'duration_sec' field.
      * @return The value.
      */
    public java.lang.Integer getDurationSec() {
      return duration_sec;
    }


    /**
      * Sets the value of the 'duration_sec' field.
      * @param value The value of 'duration_sec'.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder setDurationSec(java.lang.Integer value) {
      validate(fields()[5], value);
      this.duration_sec = value;
      fieldSetFlags()[5] = true;
      return this;
    }

    /**
      * Checks whether the 'duration_sec' field has been set.
      * @return True if the 'duration_sec' field has been set, false otherwise.
      */
    public boolean hasDurationSec() {
      return fieldSetFlags()[5];
    }


    /**
      * Clears the value of the 'duration_sec' field.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder clearDurationSec() {
      duration_sec = null;
      fieldSetFlags()[5] = false;
      return this;
    }

    /**
      * Gets the value of the 'data_volume_mb' field.
      * @return The value.
      */
    public java.lang.Double getDataVolumeMb() {
      return data_volume_mb;
    }


    /**
      * Sets the value of the 'data_volume_mb' field.
      * @param value The value of 'data_volume_mb'.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder setDataVolumeMb(java.lang.Double value) {
      validate(fields()[6], value);
      this.data_volume_mb = value;
      fieldSetFlags()[6] = true;
      return this;
    }

    /**
      * Checks whether the 'data_volume_mb' field has been set.
      * @return True if the 'data_volume_mb' field has been set, false otherwise.
      */
    public boolean hasDataVolumeMb() {
      return fieldSetFlags()[6];
    }


    /**
      * Clears the value of the 'data_volume_mb' field.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder clearDataVolumeMb() {
      data_volume_mb = null;
      fieldSetFlags()[6] = false;
      return this;
    }

    /**
      * Gets the value of the 'cell_id' field.
      * @return The value.
      */
    public java.lang.CharSequence getCellId() {
      return cell_id;
    }


    /**
      * Sets the value of the 'cell_id' field.
      * @param value The value of 'cell_id'.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder setCellId(java.lang.CharSequence value) {
      validate(fields()[7], value);
      this.cell_id = value;
      fieldSetFlags()[7] = true;
      return this;
    }

    /**
      * Checks whether the 'cell_id' field has been set.
      * @return True if the 'cell_id' field has been set, false otherwise.
      */
    public boolean hasCellId() {
      return fieldSetFlags()[7];
    }


    /**
      * Clears the value of the 'cell_id' field.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder clearCellId() {
      cell_id = null;
      fieldSetFlags()[7] = false;
      return this;
    }

    /**
      * Gets the value of the 'technology' field.
      * @return The value.
      */
    public java.lang.CharSequence getTechnology() {
      return technology;
    }


    /**
      * Sets the value of the 'technology' field.
      * @param value The value of 'technology'.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder setTechnology(java.lang.CharSequence value) {
      validate(fields()[8], value);
      this.technology = value;
      fieldSetFlags()[8] = true;
      return this;
    }

    /**
      * Checks whether the 'technology' field has been set.
      * @return True if the 'technology' field has been set, false otherwise.
      */
    public boolean hasTechnology() {
      return fieldSetFlags()[8];
    }


    /**
      * Clears the value of the 'technology' field.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder clearTechnology() {
      technology = null;
      fieldSetFlags()[8] = false;
      return this;
    }

    /**
      * Gets the value of the 'status' field.
      * @return The value.
      */
    public java.lang.CharSequence getStatus() {
      return status;
    }


    /**
      * Sets the value of the 'status' field.
      * @param value The value of 'status'.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder setStatus(java.lang.CharSequence value) {
      validate(fields()[9], value);
      this.status = value;
      fieldSetFlags()[9] = true;
      return this;
    }

    /**
      * Checks whether the 'status' field has been set.
      * @return True if the 'status' field has been set, false otherwise.
      */
    public boolean hasStatus() {
      return fieldSetFlags()[9];
    }


    /**
      * Clears the value of the 'status' field.
      * @return This builder.
      */
    public com.ensah.telecom.events.NormalizedErrorCDR.Builder clearStatus() {
      status = null;
      fieldSetFlags()[9] = false;
      return this;
    }

    @Override
    @SuppressWarnings("unchecked")
    public NormalizedErrorCDR build() {
      try {
        NormalizedErrorCDR record = new NormalizedErrorCDR();
        record.uuid = fieldSetFlags()[0] ? this.uuid : (java.lang.CharSequence) defaultValue(fields()[0]);
        record.record_type = fieldSetFlags()[1] ? this.record_type : (java.lang.CharSequence) defaultValue(fields()[1]);
        record.timestamp = fieldSetFlags()[2] ? this.timestamp : (java.time.Instant) defaultValue(fields()[2]);
        record.msisdn = fieldSetFlags()[3] ? this.msisdn : (java.lang.CharSequence) defaultValue(fields()[3]);
        record.counterparty_msisdn = fieldSetFlags()[4] ? this.counterparty_msisdn : (java.lang.CharSequence) defaultValue(fields()[4]);
        record.duration_sec = fieldSetFlags()[5] ? this.duration_sec : (java.lang.Integer) defaultValue(fields()[5]);
        record.data_volume_mb = fieldSetFlags()[6] ? this.data_volume_mb : (java.lang.Double) defaultValue(fields()[6]);
        record.cell_id = fieldSetFlags()[7] ? this.cell_id : (java.lang.CharSequence) defaultValue(fields()[7]);
        record.technology = fieldSetFlags()[8] ? this.technology : (java.lang.CharSequence) defaultValue(fields()[8]);
        record.status = fieldSetFlags()[9] ? this.status : (java.lang.CharSequence) defaultValue(fields()[9]);
        return record;
      } catch (org.apache.avro.AvroMissingFieldException e) {
        throw e;
      } catch (java.lang.Exception e) {
        throw new org.apache.avro.AvroRuntimeException(e);
      }
    }
  }

  @SuppressWarnings("unchecked")
  private static final org.apache.avro.io.DatumWriter<NormalizedErrorCDR>
    WRITER$ = (org.apache.avro.io.DatumWriter<NormalizedErrorCDR>)MODEL$.createDatumWriter(SCHEMA$);

  @Override public void writeExternal(java.io.ObjectOutput out)
    throws java.io.IOException {
    WRITER$.write(this, SpecificData.getEncoder(out));
  }

  @SuppressWarnings("unchecked")
  private static final org.apache.avro.io.DatumReader<NormalizedErrorCDR>
    READER$ = (org.apache.avro.io.DatumReader<NormalizedErrorCDR>)MODEL$.createDatumReader(SCHEMA$);

  @Override public void readExternal(java.io.ObjectInput in)
    throws java.io.IOException {
    READER$.read(this, SpecificData.getDecoder(in));
  }

}










